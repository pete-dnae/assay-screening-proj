<template>
  <transition name="fade">
    <div v-show="val" :class="['alert', 'alert-'+type, placement]" :style="{width:width}" role="alert">
      <button v-show="dismissable" type="button" class="close" @click="handleClose">
        <span>&times;</span>
      </button>
      <slot></slot>
    </div>
  </transition>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter,
.fade-leave-active {
  height: 0;
  opacity: 0;
}
.alert.top {
  position: absolute;
  top: 30px;
  margin: 0 auto;
  left: 0;
  right: 0;
  z-index: 1050;
}
.alert.top-right {
  position: absolute;
  top: 30px;
  right: 50px;
  z-index: 1050;
}
</style>
<script src="./Alert.js"></script>