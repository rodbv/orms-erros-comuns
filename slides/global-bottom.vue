<template>
  <div v-if="$nav.currentLayout !== 'cover'" class="deck-footer" aria-hidden="true">
    <div class="deck-footer__meta">
      <span>{{ $nav.currentPage }}</span>
      <span class="deck-footer__sep">/</span>
      <span>{{ $nav.total }}</span>
    </div>

    <div class="deck-footer__track">
      <div
        class="deck-footer__bar"
        :style="{ width: `${($nav.currentPage / Math.max($nav.total, 1)) * 100}%` }"
      />
    </div>
  </div>
</template>

<style scoped>
.deck-footer {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 20;
}

.deck-footer__meta {
  position: absolute;
  right: 1rem;
  bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  color: #f8fbff;
  font-size: 0.9rem;
  font-weight: 600;
  opacity: 0.9;
}

.deck-footer__sep {
  color: #feb811;
  opacity: 0.9;
}

.deck-footer__track {
  width: 100%;
  height: 4px;
  background: rgba(3, 51, 136, 0.65);
}

.deck-footer__bar {
  height: 100%;
  background: #feb811;
  transition: width 180ms ease-out;
}
</style>
