/*
 * Paper 11: Acoustic Cascades for Zero-Shot Ambient Agents
 *
 * 3-stage acoustic cascade:
 *   Stage 1: Zero-energy analog comparator (<10 uW) -> E_audio(t) > theta_analog
 *   Stage 2: 8-bit depthwise separable 15KB keyword CNN on Cortex-M0 (<200 uW) using q15_t MFCCs
 *   Stage 3: Streaming Whisper-tiny ASR on NPU (<15 mW) reading 1.5s circular ring buffer
 */

#include <stdint.h>
#include <stddef.h>

typedef int16_t q15_t;

typedef enum {
    CASCADE_STAGE_1_ANALOG_IDLE = 1,
    CASCADE_STAGE_2_CORTEX_M0_CNN = 2,
    CASCADE_STAGE_3_NPU_WHISPER = 3
} CascadeStage;

typedef struct {
    q15_t analog_threshold_q15;
    q15_t keyword_threshold_q15;
    CascadeStage current_stage;
    uint32_t ring_buffer_samples; /* 1.5s @ 16kHz = 24,000 samples */
} AcousticCascadeState;

void acoustic_cascade_init(AcousticCascadeState* state, q15_t analog_thresh, q15_t kwd_thresh) {
    if (!state) return;
    state->analog_threshold_q15 = analog_thresh;
    state->keyword_threshold_q15 = kwd_thresh;
    state->current_stage = CASCADE_STAGE_1_ANALOG_IDLE;
    state->ring_buffer_samples = 24000;
}

/* Compute fixed-point mean absolute audio energy in q15_t without FPU */
q15_t compute_audio_energy_q15(const q15_t* pcm_frame, size_t len) {
    if (!pcm_frame || len == 0) return 0;
    int32_t acc = 0;
    for (size_t i = 0; i < len; ++i) {
        int32_t sample = pcm_frame[i];
        acc += (sample < 0) ? -sample : sample;
    }
    return (q15_t)(acc / (int32_t)len);
}

CascadeStage evaluate_acoustic_cascade(
    AcousticCascadeState* state,
    const q15_t* pcm_frame,
    size_t frame_len,
    q15_t keyword_cnn_score_q15
) {
    q15_t energy = compute_audio_energy_q15(pcm_frame, frame_len);
    if (energy <= state->analog_threshold_q15) {
        state->current_stage = CASCADE_STAGE_1_ANALOG_IDLE;
        return state->current_stage;
    }
    state->current_stage = CASCADE_STAGE_2_CORTEX_M0_CNN;
    if (keyword_cnn_score_q15 > state->keyword_threshold_q15) {
        state->current_stage = CASCADE_STAGE_3_NPU_WHISPER;
    }
    return state->current_stage;
}
