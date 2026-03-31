<template>
  <Teleport to="body">
    <Transition name="dialog-show">
      <div
        v-if="visible"
        class="dialog-overlay"
        :class="[
          overlay ? 'dialog-overlay-dark' : 'no-overlay',
          `position-${position}`
        ]"
        @click.self="handleOverlayClick"
      >
        <div
          class="dialog-container"
          :style="containerStyle"
        >
          <div class="dialog-content">
            <slot name="header">
              <h3
                v-if="title"
                class="dialog-title"
                :style="{
                  textAlign: titleAlign,
                  font: titleFont,
                  color: titleColor,
                }"
              >
                {{ title }}
              </h3>
            </slot>
            <div
              class="dialog-message"
              :style="{
                textAlign: messageAlign,
                font: messageFont,
                color: messageColor,
              }"
            >
              {{ message }}
            </div>
            <slot name="footer">
              <div v-if="showButtons" class="dialog-buttons">
                <button class="dialog-btn dialog-btn-cancel" @click="handleCancel">取消</button>
                <button class="dialog-btn dialog-btn-confirm" @click="handleConfirm">确定</button>
              </div>
            </slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue'

const visible = ref(false)
const message = ref('')
const title = ref('')
const dialogWidth = ref('')      // 空字符串表示未指定
const dialogHeight = ref('')     // 空字符串表示未指定
const showButtons = ref(false)
const position = ref('center')   // 弹窗位置 str值“'center'、'top'、'bottom'、'left'、'right'、'top-left'、'top-right'、'bottom-left'、'bottom-right'”
const overlay = ref(true)        // 背景遮罩

const titleAlign = ref('left')
const messageAlign = ref('left')
const titleFont = ref('')
const titleColor = ref('')
const messageFont = ref('')
const messageColor = ref('')
const closeOnClickOverlay = ref(true)

// 自定义按钮回调
let onConfirmCallback = null
let onCancelCallback = null

let durationTimer = null
let maxDurationTimer = null
let pendingResolve = null
let pendingReject = null
let isResolved = false

// 计算弹窗容器的内联样式
const containerStyle = computed(() => {
  const style = {}
  if (dialogWidth.value) {
    style.width = dialogWidth.value
  }
  if (dialogHeight.value) {
    style.height = dialogHeight.value
  }
  return style
})

const close = (result) => {
  if (!visible.value) return

  if (durationTimer) clearTimeout(durationTimer)
  if (maxDurationTimer) clearTimeout(maxDurationTimer)
  durationTimer = null
  maxDurationTimer = null

  if (!isResolved) {
    isResolved = true
    if (result !== undefined && pendingResolve) {
      pendingResolve(result)
    } else if (pendingReject && result === undefined) {
      if (showButtons.value && !result) {
        pendingReject(new Error('Dialog timeout'))
      } else if (pendingResolve) {
        pendingResolve(result)
      }
    }
  }

  pendingResolve = null
  pendingReject = null
  visible.value = false
}

const handleConfirm = () => {
  if (onConfirmCallback) {
    onConfirmCallback({
      message: message.value,
      title: title.value,
      showButtons: showButtons.value
    })
  }
  close('confirm')
}

const handleCancel = () => {
  if (onCancelCallback) {
    onCancelCallback({
      message: message.value,
      title: title.value,
      showButtons: showButtons.value
    })
  }
  close('cancel')
}

const handleOverlayClick = () => {
  if (!closeOnClickOverlay.value) return
  if (showButtons.value) {
    close('cancel')
  } else {
    close()
  }
}

const open = (options) => {
  if (visible.value) close()

  const {
    message: msg,
    title: ttl = '',
    width = '',           // 默认空字符串 → 自适应
    height = '',          // 默认空字符串 → 自适应
    showButtons: btns = false,
    duration = 2000,
    maxDuration = 0,
    hasReturnValue = false,
    position: pos = 'center',
    overlay: ov = true,
    // 字体样式参数
    titleAlign: tAlign = 'left',
    messageAlign: mAlign = 'left',
    titleFont: tFont = '',
    titleColor: tColor = '',
    messageFont: mFont = '',
    messageColor: mColor = '',
    closeOnClickOverlay: cOverlay = undefined,
    // 自定义按钮回调
    onConfirm = null,
    onCancel = null,
  } = options

  message.value = msg
  title.value = ttl
  dialogWidth.value = width
  dialogHeight.value = height
  showButtons.value = btns
  position.value = pos
  overlay.value = ov
  titleAlign.value = tAlign
  messageAlign.value = mAlign
  titleFont.value = tFont
  titleColor.value = tColor
  messageFont.value = mFont
  messageColor.value = mColor

  if (cOverlay !== undefined) {
    closeOnClickOverlay.value = cOverlay
  } else {
    closeOnClickOverlay.value = ov
  }

  // 存储自定义回调
  onConfirmCallback = onConfirm
  onCancelCallback = onCancel

  isResolved = false
  pendingResolve = null
  pendingReject = null

  visible.value = true

  const promise = new Promise((resolve, reject) => {
    pendingResolve = resolve
    pendingReject = reject
  })

  if (!btns && duration > 0) {
    durationTimer = setTimeout(() => close(), duration)
  }

  if (btns && maxDuration > 0) {
    maxDurationTimer = setTimeout(() => close('timeout'), maxDuration)
  }

  return promise
}

defineExpose({ open })
</script>

<style scoped>

/* 过渡动画（淡入淡出 + 缩放） */
.dialog-show-enter-active,
.dialog-show-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.dialog-show-enter-from,
.dialog-show-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.dialog-show-enter-to,
.dialog-show-leave-from {
  opacity: 1;
  transform: scale(1);
}

/* 遮罩层基础样式 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  z-index: 1000;
}

/* 背景遮罩样式 */
.dialog-overlay-dark {
  background-color: rgba(0, 0, 0, 0.5);
}

/* 无遮罩层样式（完全透明，不阻挡点击） */
.no-overlay {
  background-color: transparent;
  pointer-events: none;
}

/* ========== 位置预设 ========== */
.position-center {
  align-items: center;
  justify-content: center;
}
.position-top {
  align-items: flex-start;
  justify-content: center;
  padding-top: 20px;
}
.position-bottom {
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 20px;
}
.position-left {
  align-items: center;
  justify-content: flex-start;
  padding-left: 20px;
}
.position-right {
  align-items: center;
  justify-content: flex-end;
  padding-right: 20px;
}
.position-top-left {
  align-items: flex-start;
  justify-content: flex-start;
  padding: 20px;
}
.position-top-right {
  align-items: flex-start;
  justify-content: flex-end;
  padding: 20px;
}
.position-bottom-left {
  align-items: flex-end;
  justify-content: flex-start;
  padding: 20px;
}
.position-bottom-right {
  align-items: flex-end;
  justify-content: flex-end;
  padding: 20px;
}

/* 弹窗容器自适应样式 */
.dialog-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  /* 自适应宽度：最小200px，最大90vw，由内容撑开 */
  width: auto;
  min-width: 200px;
  max-width: 60vw;
  /* 自适应高度：最大60vh，内容决定高度 */
  height: auto;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  /* 确保弹窗容器可点击（覆盖父级 pointer-events: none） */
  pointer-events: auto;
}

.dialog-content {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

/* 默认样式（未提供自定义时使用） */
.dialog-title {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 1.2rem;
  font-weight: 600;
  color: #1f2937;
}

.dialog-message {
  margin-bottom: 20px;
  line-height: 1.5;
  color: #374151;
}

.dialog-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}

.dialog-btn {
  padding: 6px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.dialog-btn-cancel {
  background-color: #f0f0f0;
  color: #333;
}
.dialog-btn-cancel:hover {
  background-color: #e0e0e0;
}

.dialog-btn-confirm {
  background-color: #1890ff;
  color: white;
}
.dialog-btn-confirm:hover {
  background-color: #40a9ff;
}

/* ========== 夜间模式支持 ========== */
.dark .dialog-container {
  background: #1f2937;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.5);
}
.dark .dialog-title {
  color: #f3f4f6;
}
.dark .dialog-message {
  color: #d1d5db;
}
.dark .dialog-btn-cancel {
  background-color: #374151;
  color: #e5e7eb;
}
.dark .dialog-btn-cancel:hover {
  background-color: #4b5563;
}
.dark .dialog-btn-confirm {
  background-color: #3b82f6;
}
.dark .dialog-btn-confirm:hover {
  background-color: #60a5fa;
}

/* 过渡动画 */
.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity 0.3s ease;
}
.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;
}
.dialog-fade-enter-to,
.dialog-fade-leave-from {
  opacity: 1;
}
</style>