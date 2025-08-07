<template>
  <div
    :style="{
      '--border-width': `${borderWidth}px`,
      '--duration': `${duration}s`,
      '--shine-color': color,
      '--radius': `${borderRadius}px`
    }"
    class="shine-border-wrapper"
  >
    <div class="shine-border-content">
      <slot></slot>
    </div>
    <div class="shine-border-effect"></div>
  </div>
</template>

<script setup>
defineProps({
  borderWidth: {
    type: Number,
    default: 1
  },
  duration: {
    type: Number,
    default: 8
  },
  color: {
    type: String,
    default: '#fff'
  },
  borderRadius: {
    type: Number,
    default: 12
  }
})
</script>

<style scoped>
@keyframes shine {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.shine-border-wrapper {
  position: relative;
  border-radius: var(--radius);
  overflow: hidden;
  padding: var(--border-width);
}

.shine-border-content {
  position: relative;
  z-index: 1;
  border-radius: calc(var(--radius) - var(--border-width));
  overflow: hidden;
  width: 100%;
  height: 100%;
}

.shine-border-effect {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    110deg,
    transparent 20%,
    var(--shine-color) 50%,
    transparent 80%
  );
  background-size: 200% 100%;
  animation: shine var(--duration) linear infinite;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
  z-index: 0;
}

.shine-border-wrapper:hover .shine-border-effect {
  opacity: 1;
}
</style> 