import importlib
import numpy as np
from sklearn.cluster import KMeans


def cluster_images(image_data, n_clusters=5, random_state=42):
    #Make clutser from the images
    if not image_data:
        return []

    # Adjust cluster count if total images fewer than requested clusters
    k = min(n_clusters, len(image_data))
    vectors = np.array([item["vector"] for item in image_data])

    kmeans = KMeans(n_clusters=k, random_state=random_state, n_init="auto")
    labels = kmeans.fit_predict(vectors)
    centroids = kmeans.cluster_centers_

    # Group images into their assigned clusters
    grouped = {cluster_id: [] for cluster_id in range(k)}
    for item, label in zip(image_data, labels):
        centroid = centroids[label]
        distance = float(np.linalg.norm(item["vector"] - centroid))

        photo_entry = {
            **item,
            "cluster_id": int(label),
            "distance_to_centroid": round(distance, 4)
        }
        grouped[int(label)].append(photo_entry)

    # Build final cluster list sorted by cluster_id and internal rank
    clusters = []
    for cluster_id in range(k):
        # Closest image to centroid ranks #1 (most representative)
        sorted_photos = sorted(
            grouped[cluster_id],
            key=lambda x: x["distance_to_centroid"]
        )
        for rank, photo in enumerate(sorted_photos, start=1):
            photo["rank"] = rank

        clusters.append({
            "cluster_id": cluster_id,
            "count": len(sorted_photos),
            "centroid": centroids[cluster_id],
            "photos": sorted_photos
        })

    return clusters


if __name__ == "__main__":
    # Use importlib because module filename starts with a digit ('1_')
    extractor = importlib.import_module("1_color_extractor")
    data = extractor.process_folder("images")

    clusters = cluster_images(data, n_clusters=5)
    print(f"Created {len(clusters)} color/light clusters from {len(data)} images:\n")