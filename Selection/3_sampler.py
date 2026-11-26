import os
import shutil
import importlib
import numpy as np
from PIL import Image, ImageFilter
from pillow_heif import register_heif_opener
from sklearn.cluster import KMeans

register_heif_opener()


def _measure_raw_quality(filepath, hero_eligible):
    """
    Compute raw image quality metrics using Pillow & NumPy:
      - sharpness_raw
      - exposure_score
      - res_score: bonus for high resolution (>= 1200px)
    """
    with Image.open(filepath) as img:
        gray = img.convert("L")
        gray.thumbnail((512, 512))
        arr = np.asarray(gray, dtype=np.float32)

        # 1. Sharpness via edge detection variance
        edges = gray.filter(ImageFilter.FIND_EDGES)
        sharpness_raw = float(np.var(np.asarray(edges, dtype=np.float32)))

        # 2. Exposure & contrast balance
        mean_lum = float(np.mean(arr)) / 255.0
        brightness_balance = max(0.0, 1.0 - abs(mean_lum - 0.5) * 2.0)
        contrast_score = min(float(np.std(arr)) / 128.0, 1.0)
        exposure_score = 0.5 * brightness_balance + 0.5 * contrast_score

    # 3. Print resolution readiness
    res_score = 1.0 if hero_eligible else 0.4

    return sharpness_raw, exposure_score, res_score


def select_subcluster_representatives(clusters, max_subclusters=4, random_state=42):
    """
    Split each main cluster into sub-clusters #to get distinctive representation
    and pick the highest-quality photo from each.
    """
    for cluster in clusters:
        photos = cluster["photos"]
        if not photos:
            cluster["candidates"] = []
            continue

        # Measure raw quality for every photo in the cluster
        raw_metrics = {}
        for p in photos:
            raw_metrics[p["filename"]] = _measure_raw_quality(
                p["filepath"], p["hero_eligible"]
            )

        max_sharpness = max(m[0] for m in raw_metrics.values()) or 1.0

        # Adaptive sub-cluster count: never exceed actual photo count
        k_sub = min(max_subclusters, len(photos))

        if k_sub == 1:
            sub_groups = {0: [(photos[0], 0.0)]}
        else:
            sub_vecs = np.array([p["vector"] for p in photos])
            sub_km = KMeans(n_clusters=k_sub, random_state=random_state, n_init="auto")
            sub_labels = sub_km.fit_predict(sub_vecs)
            sub_centroids = sub_km.cluster_centers_

            sub_groups = {s: [] for s in range(k_sub)}
            for p, slabel in zip(photos, sub_labels):
                dist = float(np.linalg.norm(p["vector"] - sub_centroids[slabel]))
                sub_groups[int(slabel)].append((p, dist))

        # Order sub-clusters by size descending so the largest scene appears first
        ordered_subgroups = sorted(
            [(sid, grp) for sid, grp in sub_groups.items() if grp],
            key=lambda item: len(item[1]),
            reverse=True
        )

        candidates = []
        for idx, (_, grp) in enumerate(ordered_subgroups):
            max_dist = max(d for _, d in grp) or 1.0

            def candidate_score(item):
                photo, dist = item
                sharp_raw, exp_score, res_score = raw_metrics[photo["filename"]]
                sharp_norm = sharp_raw / max_sharpness
                # Weighted technical quality + slight centrality tie-breaker
                quality = (0.50 * sharp_norm) + (0.30 * exp_score) + (0.20 * res_score)
                centrality_penalty = 0.05 * (dist / max_dist)
                return quality - centrality_penalty

            best_photo, best_dist = max(grp, key=candidate_score)
            sharp_raw, exp_score, res_score = raw_metrics[best_photo["filename"]]
            final_q = (
                0.50 * (sharp_raw / max_sharpness)
                + 0.30 * exp_score
                + 0.20 * res_score
            )

            candidates.append({
                **best_photo,
                "sub_cluster": idx + 1,
                "quality_score": round(float(final_q), 4),
                "page": 1 if idx == 0 else 2,
                "role": "hero" if idx == 0 else "story_spread"
            })

        cluster["candidates"] = candidates

    return clusters


def export_candidate_samples(clusters, sample_dir="output/samples", max_size=512):
    """
    Convert the selected sub-cluster candidate photos into lightweight JPEGs.
    Before sendig them to LLM inputs and UI preview thumbnails.
    """
    if os.path.exists(sample_dir):
        shutil.rmtree(sample_dir)
    os.makedirs(sample_dir, exist_ok=True)

    for cluster in clusters:
        cid = cluster["cluster_id"]
        sample_paths = []

        for idx, photo in enumerate(cluster.get("candidates", [])):
            base_name = os.path.splitext(photo["filename"])[0]
            out_name = f"cluster_{cid}_cand_{idx}_{base_name}.jpg"
            out_path = os.path.join(sample_dir, out_name)

            with Image.open(photo["filepath"]) as img:
                img_rgb = img.convert("RGB")
                img_rgb.thumbnail((max_size, max_size))
                img_rgb.save(out_path, "JPEG", quality=85)

            clean_path = out_path.replace("\\", "/")
            photo["llm_sample_path"] = clean_path
            sample_paths.append(clean_path)

        cluster["llm_sample_paths"] = sample_paths

    return clusters


def build_initial_chapters(selected_clusters):
    """
    Assemble chapter photo lists from the selected clusters while ensuring
    zero duplicate filenames across chapters.
    """
    used_filenames = set()
    chapters = []

    for chapter_idx, cluster in enumerate(selected_clusters, start=1):
        chapter_photos = []
        for photo in cluster.get("candidates", []):
            if photo["filename"] not in used_filenames:
                chapter_photos.append({**photo})
                used_filenames.add(photo["filename"])

        if chapter_photos:
            chapters.append({
                "chapter_number": chapter_idx,
                "cluster_id": cluster["cluster_id"],
                "photos": chapter_photos
            })

    return chapters, used_filenames


def get_photo_pool(all_clusters, used_filenames, anchor_photo=None):
    """
    Gather all unselected photos into the Photo Pool.
    If anchor_photo is provided (after a user swap), re-rank remaining photos
    by vector similarity to the anchor photo.
    """
    pool = []
    seen = set()

    for cluster in all_clusters:
        for p in cluster["photos"]:
            fname = p["filename"]
            if fname not in used_filenames and fname not in seen:
                seen.add(fname)
                entry = {**p}
                if anchor_photo is not None:
                    dist = float(np.linalg.norm(p["vector"] - anchor_photo["vector"]))
                    entry["similarity_distance"] = round(dist, 4)
                pool.append(entry)

    if anchor_photo is not None:
        pool.sort(key=lambda x: x["similarity_distance"])
    else:
        pool.sort(key=lambda x: x["distance_to_centroid"])

    return pool


if __name__ == "__main__":
    extractor = importlib.import_module("1b_clip_extractor")
    clustering = importlib.import_module("2_clustering")

    data = extractor.process_folder("images")
    clusters = clustering.cluster_images(data, n_clusters=4)
    clusters = select_subcluster_representatives(clusters, max_subclusters=4)