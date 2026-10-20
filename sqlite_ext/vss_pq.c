/*
 * Paper 09: Edge-Native Vector Indexing via Quantized Product Quantization in Memory-Mapped SQLite
 *
 * Implements Asymmetric Distance Computation (ADC) with 4-bit / 8-bit PQ lookup tables:
 *   d_ADC(q, x)^2 = \sum_{m=1}^M || q^{(m)} - c_{i_m}^{(m)} ||^2
 * Precomputes D_lut \in R^{M \times K} so each row scan performs only M table lookups and additions.
 */

#include <stdint.h>
#include <stddef.h>

#define VSS_PQ_MAX_SUBVECTORS 64
#define VSS_PQ_CENTROID_COUNT 16 /* 4-bit codebooks (2^4 = 16 centroids per subvector) */

typedef struct {
    uint32_t dimensions;
    uint32_t subvectors;
    uint32_t bits_per_code;
    float distance_lut[VSS_PQ_MAX_SUBVECTORS][VSS_PQ_CENTROID_COUNT];
} VssPqContext;

/* Precompute M x 16 distance lookup table for an unquantized query vector q */
void vss_pq_precompute_lut(
    VssPqContext* ctx,
    const float* query,
    const float* codebooks /* shape: [M][16][D/M] */
) {
    uint32_t sub_dim = ctx->dimensions / ctx->subvectors;
    for (uint32_t m = 0; m < ctx->subvectors; ++m) {
        const float* q_sub = query + (m * sub_dim);
        for (uint32_t c = 0; c < VSS_PQ_CENTROID_COUNT; ++c) {
            const float* centroid = codebooks + ((m * VSS_PQ_CENTROID_COUNT + c) * sub_dim);
            float dist_sq = 0.0f;
            for (uint32_t d = 0; d < sub_dim; ++d) {
                float diff = q_sub[d] - centroid[d];
                dist_sq += diff * diff;
            }
            ctx->distance_lut[m][c] = dist_sq;
        }
    }
}

/* Evaluate ADC squared distance using packed 4-bit PQ codes (2 subvectors per byte) */
float vss_pq_adc_distance_4bit(const VssPqContext* ctx, const uint8_t* packed_codes) {
    float total = 0.0f;
    for (uint32_t m = 0; m < ctx->subvectors; m += 2) {
        uint8_t byte_val = packed_codes[m >> 1];
        uint8_t code_lo = byte_val & 0x0F;
        uint8_t code_hi = (byte_val >> 4) & 0x0F;
        total += ctx->distance_lut[m][code_lo];
        if (m + 1 < ctx->subvectors) {
            total += ctx->distance_lut[m + 1][code_hi];
        }
    }
    return total;
}
