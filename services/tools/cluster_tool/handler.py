import json
import numpy as np
from typing import Tuple

def _kmeans_plus_plus_init(X: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    n, _ = X.shape
    centers = np.empty((k, X.shape[1]), dtype=X.dtype)
    idx = rng.integers(0, n)
    centers[0] = X[idx]
    closest_dist_sq = np.sum((X - centers[0]) ** 2, axis=1)
    for i in range(1, k):
        probs = closest_dist_sq / np.sum(closest_dist_sq)
        idx = rng.choice(n, p=probs)
        centers[i] = X[idx]
        dist_sq = np.sum((X - centers[i]) ** 2, axis=1)
        closest_dist_sq = np.minimum(closest_dist_sq, dist_sq)
    return centers

def _kmeans(X: np.ndarray, k: int, max_iter: int = 100, tol: float = 1e-4, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    centers = _kmeans_plus_plus_init(X, k, rng)

    for _ in range(max_iter):
        dists = np.linalg.norm(X[:, None, :] - centers[None, :, :], axis=2)
        labels = np.argmin(dists, axis=1)
        new_centers = centers.copy()
        for j in range(k):
            pts = X[labels == j]
            if len(pts) > 0:
                new_centers[j] = pts.mean(axis=0)
        if np.linalg.norm(new_centers - centers) < tol:
            break
        centers = new_centers
    return labels, centers

def handler(event, _):
    embs = np.array(event["inputs"]["embeddings"], dtype=np.float32)
    n = embs.shape[0]
    k = max(2, min(8, max(2, n // 3)))
    labels, _ = _kmeans(embs, k=k, max_iter=100, tol=1e-4, seed=42)
    return {"clusters": labels.astype(int).tolist()}

