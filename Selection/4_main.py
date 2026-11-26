import os
import sys
import json
import importlib


def clean_photo_metadata(photo):
    """Strip raw numpy vectors so photo metadata can be serialized cleanly to JSON."""
    cleaned = {k: v for k, v in photo.items() if k != "vector"}
    if "filepath" in cleaned:
        cleaned["filepath"] = cleaned["filepath"].replace("\\", "/")
    return cleaned


def run_selection_pipeline(
    lens="clip",
    image_dir="images",
    n_clusters=4,
    max_subclusters=4
):
    
    if lens == "color":
        extractor = importlib.import_module("1_color_extractor")
        lens_type = "color_light_hsv"
    elif lens == "clip":
        extractor = importlib.import_module("1b_clip_extractor")
        lens_type = "semantic_clip"
    else:
        raise ValueError("Invalid lens. Choose 'color' or 'clip'.")

    clustering = importlib.import_module("2_clustering")
    sampler = importlib.import_module("3_sampler")

    clusters_json = f"output/clusters_{lens}.json"
    sample_dir = f"output/samples_{lens}"
    output_json = f"output/selection_{lens}.json"

    # Step 1: Extract vectors and metadata
    print(f"[1/4] Extracting {lens_type} vectors from '{image_dir}'...")
    image_data = extractor.process_folder(image_dir)
    if not image_data:
        raise ValueError("No valid images found to process.")

    # Step 2: Main clustering & save initial clusters JSON
    print(f"[2/4] Clustering {len(image_data)} images into {n_clusters} main groups...")
    clusters = clustering.cluster_images(image_data, n_clusters=n_clusters)

    os.makedirs(os.path.dirname(clusters_json), exist_ok=True)
    clusters_payload = {
        "lens_type": lens_type,
        "total_images_processed": len(image_data),
        "n_clusters": len(clusters),
        "clusters": [
            {
                "cluster_id": c["cluster_id"],
                "photo_count": c["count"],
                "photos": [clean_photo_metadata(p) for p in c["photos"]]
            }
            for c in clusters
        ]
    }
    with open(clusters_json, "w", encoding="utf-8") as f:
        json.dump(clusters_payload, f, indent=2)
    print(f"      Saved initial clustering result to '{clusters_json}'.")

    # Step 3: Adaptive sub-clustering + quality selection + JPEG export
    print(f"[3/4] Picking up to {max_subclusters} high-quality sub-cluster representatives...")
    clusters = sampler.select_subcluster_representatives(clusters, max_subclusters=max_subclusters)
    clusters = sampler.export_candidate_samples(clusters, sample_dir=sample_dir)

    # Step 4: Populate default first 3 chapters & remaining Photo Pool
    print("[4/4] Building initial chapters and Photo Pool...")
    initial_selection = clusters[:3]
    chapters, used_filenames = sampler.build_initial_chapters(initial_selection)
    photo_pool = sampler.get_photo_pool(clusters, used_filenames)

    payload = {
        "lens_type": lens_type,
        "total_images_processed": len(image_data),
        "theme_options": [
            {
                "cluster_id": c["cluster_id"],
                "photo_count": c["count"],
                "theme_title": f"{lens.capitalize()} Theme {c['cluster_id'] + 1}",
                "theme_description": "Pending Vision-LLM description from candidate images.",
                "hero_index": 0,
                "llm_sample_paths": c["llm_sample_paths"],
                "candidate_photos": [clean_photo_metadata(p) for p in c["candidates"]]
            }
            for c in clusters
        ],
        "selected_chapters": [
            {
                "chapter_number": ch["chapter_number"],
                "cluster_id": ch["cluster_id"],
                "photos": [clean_photo_metadata(p) for p in ch["photos"]]
            }
            for ch in chapters
        ],
        "photo_pool": [clean_photo_metadata(p) for p in photo_pool]
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"\nDone! Final selection output saved to '{output_json}'.")
    print(f"- Initial clusters JSON   : {clusters_json}")
    print(f"- Theme options generated : {len(payload['theme_options'])}")
    print(f"- Chapters populated      : {len(payload['selected_chapters'])}")
    print(f"- Remaining in Photo Pool : {len(payload['photo_pool'])}")


if __name__ == "__main__":
    selected_lens = sys.argv[1].lower() if len(sys.argv) > 1 else "clip"
    run_selection_pipeline(
        lens=selected_lens,
        image_dir="images",
        n_clusters=4,
        max_subclusters=4
    )