<template>
  <div v-if="$nav.currentLayout !== 'cover'" class="deck-overlay" aria-hidden="true">
    <img src="/logo.png" alt="" class="deck-overlay__logo" />
  </div>

  <div v-if="$nav.currentLayout !== 'cover'" class="deck-footer" aria-hidden="true">
    <div class="deck-footer__microcopy">Python Floripa #93</div>

    <div class="deck-footer__track">
      <div
        class="deck-footer__bar"
        :style="{ width: `${($nav.currentPage / Math.max($nav.total, 1)) * 100}%` }"
      />
    </div>
  </div>
</template>

<style scoped>
.deck-overlay {
  position: fixed;
  right: 1rem;
  bottom: 0.65rem;
  pointer-events: none;
  z-index: 21;
}

.deck-overlay__logo {
  display: block;
  width: 63px;
  height: auto;
  opacity: 0.95;
}

.deck-footer {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 20;
}

.deck-footer__microcopy {
  position: absolute;
  left: 1rem;
  bottom: 0.5rem;
  color: #f8fbff;
  font-size: 0.5rem;
  font-weight: 500;
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  letter-spacing: 0.01em;
  opacity: 0.8;
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
