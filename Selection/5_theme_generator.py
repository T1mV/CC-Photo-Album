import os
import sys
import json
import time
import random
from PIL import Image
from pydantic import BaseModel
from google import genai
from google.genai import types
from google.genai.errors import APIError


class ClusterCuration(BaseModel):
    cluster_id: int
    theme_title: str
    theme_description: str
    hero_index: int


class AllChaptersCuration(BaseModel):
    chapters: list[ClusterCuration]


def generate_with_retry(client, contents, schema, model_name="gemini-3.5-flash-lite", max_retries=6):
    """Call Gemini Vision with exponential backoff + jitter on 503/429 server spikes."""
    for attempt in range(1, max_retries + 1):
        try:
            return client.models.generate_content(
                model=model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.75
                )
            )
        except APIError as e:
            if e.code in (429, 503) and attempt < max_retries:
                wait_sec = (attempt * 3) + round(random.uniform(0.5, 1.5), 1)
                print(f"  [Warning] {model_name} busy (HTTP {e.code}). Retrying in {wait_sec}s...")
                time.sleep(wait_sec)
            else:
                raise


def _apply_hero_selection(candidates, hero_idx):
    """
    Validate hero_idx (preferring hero_eligible photos if out of range),
    assign Page 1 (hero) vs Page 2 (story_spread), and place Hero first.
    """
    if not candidates:
        return [], 0

    if not (0 <= hero_idx < len(candidates)):
        eligible_indices = [i for i, p in enumerate(candidates) if p.get("hero_eligible")]
        hero_idx = eligible_indices[0] if eligible_indices else 0

    hero_photo = {**candidates[hero_idx], "page": 1, "role": "hero"}
    spread_photos = [
        {**p, "page": 2, "role": "story_spread"}
        for i, p in enumerate(candidates)
        if i != hero_idx
    ]
    return [hero_photo, *spread_photos], hero_idx


def generate_themes_from_json(json_path="output/selection_clip.json"):
    """
    Send all clusters' candidate photos together in ONE batched Gemini Vision call
    so chapter titles are mutually distinct, non-repetitive, and Hero-curated.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"'{json_path}' not found. Run 4_main.py first.")

    if not os.environ.get("GEMINI_API_KEY"):
        raise EnvironmentError(
            "GEMINI_API_KEY is not set. Run: $env:GEMINI_API_KEY='your_api_key' in PowerShell."
        )

    with open(json_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    client = genai.Client()
    lens_type = payload.get("lens_type", "unknown")
    theme_options = payload.get("theme_options", [])

    if not theme_options:
        print("No theme options found in JSON.")
        return

    prompt_intro = (
        "You are an editorial photobook designer curating a multi-chapter book from one trip. "
        f"Below are {len(theme_options)} distinct photo clusters (grouped by: {lens_type}). "
        "Compare all clusters side-by-side and generate a distinct chapter identity for each one.\n\n"
        "Strict rules:\n"
        "1. 'theme_title' (2 to 4 words): Make every chapter title sharply distinct in focus and mood "
        "(e.g., portraits/moments vs. street details vs. hilltop panoramas vs. riverside night lights). "
        "NEVER repeat the same buzzwords (such as 'Winter', 'Journey', 'Explorer', or city names) across multiple titles.\n"
        "2. 'theme_description': One vivid sentence explaining what makes this specific chapter unique compared to the others.\n"
        "3. 'hero_index': Integer index (0 to N-1) of the strongest full-page Page 1 Hero photo for that cluster "
        "(strongly prefer images marked 'high-res print ready').\n"
    )

    multimodal_contents = [prompt_intro]

    for option in theme_options:
        cid = option["cluster_id"]
        candidates = option.get("candidate_photos", [])
        multimodal_contents.append(
            f"\n=== CLUSTER {cid} ({option['photo_count']} total photos in cluster) ==="
        )

        for idx, cand in enumerate(candidates):
            path = cand.get("llm_sample_path", "")
            if os.path.exists(path):
                with Image.open(path) as img:
                    res_tag = "high-res print ready" if cand.get("hero_eligible") else "standard resolution"
                    multimodal_contents.append(
                        f"Cluster {cid} - Image {idx}: {cand['filename']} ({cand['orientation']}, {res_tag})"
                    )
                    multimodal_contents.append(img.copy())

    print(f"Sending all {len(theme_options)} clusters in 1 batched call to Gemini Vision (lens: {lens_type})...\n")

    response = generate_with_retry(
        client=client,
        contents=multimodal_contents,
        schema=AllChaptersCuration,
        model_name="gemini-3.5-flash-lite"
    )

    result = json.loads(response.text)
    curation_map = {item["cluster_id"]: item for item in result.get("chapters", [])}

    for option in theme_options:
        cid = option["cluster_id"]
        curation = curation_map.get(cid)
        if not curation:
            continue

        candidates = option.get("candidate_photos", [])
        ordered_candidates, valid_hero_idx = _apply_hero_selection(
            candidates, int(curation["hero_index"])
        )

        option["theme_title"] = curation["theme_title"]
        option["theme_description"] = curation["theme_description"]
        option["hero_index"] = valid_hero_idx
        option["candidate_photos"] = ordered_candidates

        # Sync updated Hero + Spread order into selected_chapters if active
        for ch in payload.get("selected_chapters", []):
            if ch["cluster_id"] == cid:
                ch["photos"] = [dict(p) for p in ordered_candidates]

        hero_photo = ordered_candidates[0]
        print(f"=== Cluster {cid} ({option['photo_count']} photos) ===")
        print(f"  Title       : {option['theme_title']}")
        print(f"  Description : {option['theme_description']}")
        print(f"  Hero (Pg 1) : {hero_photo['filename']} ({hero_photo['orientation']})")
        print(f"  Spread (Pg2): {[p['filename'] for p in ordered_candidates[1:]]}\n")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"All done! Saved distinct chapter themes to '{json_path}'.")


if __name__ == "__main__":
    target_json = sys.argv[1] if len(sys.argv) > 1 else "output/selection_clip.json"
    generate_themes_from_json(target_json)