<template>
  <svg
    aria-hidden="true"
    class="pointer-events-none absolute inset-0 h-full w-full fill-gray-400/30 stroke-gray-400/30"
  >
    <defs>
      <pattern
        :id="id"
        :width="width"
        :height="height"
        patternUnits="userSpaceOnUse"
        :x="x"
        :y="y"
      >
        <path :d="`M.5 ${height}V.5H${width}`" fill="none" />
      </pattern>
    </defs>
    <rect width="100%" height="100%" stroke-width="0" :fill="`url(#${id})`" />
  </svg>
</template>

<script setup>
import { ref } from 'vue'

// Generate a unique ID for the pattern
const id = ref(`grid-pattern-${Math.random().toString(36).substr(2, 9)}`)

defineProps({
  width: {
    type: Number,
    default: 40
  },
  height: {
    type: Number,
    default: 40
  },
  x: {
    type: Number,
    default: -1
  },
  y: {
    type: Number,
    default: -1
  }
})
</script> 