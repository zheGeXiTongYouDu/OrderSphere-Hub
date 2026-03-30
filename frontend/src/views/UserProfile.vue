<template>
  <div class="max-w-3xl mx-auto mt-10 bg-white dark:bg-gray-800 p-6 rounded shadow">
    <h2 class="text-2xl font-bold mb-4 text-center text-gray-900 dark:text-white">编辑个人资料</h2>

    <!-- 账户信息行（邮箱/登出/修改密码）- 简化展示 -->
    <div class="mb-6">
      <div class="flex items-center justify-between">
        <div>
          <div class="text-sm text-gray-600 dark:text-gray-300">登录邮箱</div>
          <div class="font-medium text-gray-800 dark:text-gray-100">{{ userEmail || '未设置' }}</div>
        </div>

        <div class="flex items-center space-x-3">
          <button @click="logout" class="bt_sml_defa">退出登录</button>
          <button @click="goChangePassword" class="bt_sml_defa">修改密码</button>
        </div>
      </div>
    </div>

    <form @submit.prevent="onSubmit" class="space-y-6">
      <!-- 用户名 显示 / 修改 布局（保留原有结构） -->
      <table class="w-full">
        <tbody>
          <tr>
            <td style="padding-top:8px;text-align:right;width:25%" class="text-gray-700 dark:text-gray-200">
              用户名 :
            </td>
            <td style="padding-top:8px;text-align:left;width:75%">
              <!-- 显示模式 -->
              <div v-if="!editingNick" id="div_nickname_display">
                <span class="mr-4 font-medium text-gray-800 dark:text-gray-100">{{ username }}</span>
                <button type="button" class="bt_sml_defa" @click="dispNickChange">修改昵称</button>
              </div>

              <!-- 修改模式 -->
              <div v-else id="div_nickname_change">
                <input
                  v-model="tempNickname"
                  @input="onNickInput"
                  type="text"
                  name="nickname"
                  maxlength="32"
                  class="input_sml"
                  style="width:200px;"
                />
                <button type="button" @click="confirmNickChange" class="bt_sml_main ml-2">确认修改</button>
                <button type="button" @click="cancelNickChange" class="bt_sml_defa_narr ml-2">取消</button>

                <div class="mt-2">
                  <p v-if="checking" class="text-xs text-gray-500 dark:text-gray-400">检查中...</p>
                  <p v-else-if="tempNickname && nickAvailable === true" class="text-xs text-green-600 dark:text-green-400">该用户名可用</p>
                  <p v-else-if="tempNickname && nickAvailable === false" class="text-xs text-red-600 dark:text-red-400">该用户名已被占用</p>
                </div>
              </div>
            </td>
          </tr>

          <!-- 头像上传区域 -->
          <tr>
            <td style="padding-top:18px;text-align:right;width:25%" class="text-gray-700 dark:text-gray-200">
              头像 :
            </td>
            <td style="padding-top:18px;text-align:left;width:75%">
              <div class="flex items-start space-x-4">
                <div class="w-24 h-24 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-700 flex-shrink-0">
                  <img :src="currentAvatar" alt="avatar" class="w-full h-full object-cover" />
                </div>

                <div class="flex-1">
                  <div class="mb-2 text-sm text-gray-600 dark:text-gray-300">上传头像（仅支持正方形图片，将被缩放为 100×100）</div>
                  <input type="file" accept="image/*" @change="onAvatarFileChange" class="text-sm text-gray-700 dark:text-gray-200" />
                  <div class="mt-2 space-x-2">
                    <button v-if="selectedBlob" type="button" @click="uploadAvatar" class="bt_sml_main">上传头像</button>
                    <button v-if="selectedBlob" type="button" @click="clearAvatarSelection" class="bt_sml_defa_narr">取消</button>
                  </div>

                  <p v-if="avatarError" class="text-red-500 text-sm mt-2">{{ avatarError }}</p>
                  <p v-if="avatarSuccess" class="text-green-600 text-sm mt-2">{{ avatarSuccess }}</p>
                  <p v-if="avatarInfo" class="text-xs text-gray-500 dark:text-gray-400 mt-2">{{ avatarInfo }}</p>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div>
        <p v-if="error" class="text-red-500 text-sm mt-2">{{ error }}</p>
        <p v-if="success" class="text-green-600 text-sm mt-2">{{ success }}</p>
      </div>
    </form>
  </div>
</template>

<script setup>
import {ref, computed} from 'vue'
import {useRouter} from 'vue-router'
import {useUserStore} from '../store/user'

// 简单防抖函数
function debounce(fn, wait = 300) {
  let timeout = null
  return function (...args) {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => fn.apply(this, args), wait)
  }
}

const user = useUserStore()
const router = useRouter()

// --- username related (保留原有逻辑) ---
const username = ref(user.username || '')
const tempNickname = ref(username.value)
const editingNick = ref(false)
const nickAvailable = ref(null)
const checking = ref(false)
const error = ref('')
const success = ref('')
const userEmail = user.email || ''

async function checkNickname(name) {
  if (!name || name === user.username) {
    nickAvailable.value = null
    checking.value = false
    return
  }
  checking.value = true
  nickAvailable.value = null
  try {
    const res = await fetch(`http://127.0.0.1:8000/auth/check-username?username=${encodeURIComponent(name)}`)
    if (!res.ok) {
      nickAvailable.value = null
    } else {
      const data = await res.json()
      nickAvailable.value = !!data.available
    }
  } catch (e) {
    nickAvailable.value = null
  } finally {
    checking.value = false
  }
}

const debouncedNickCheck = debounce((val) => checkNickname(val), 400)

function dispNickChange() {
  tempNickname.value = username.value
  editingNick.value = true
  nickAvailable.value = null
  error.value = ''
  success.value = ''
}

function cancelNickChange() {
  editingNick.value = false
  tempNickname.value = username.value
  nickAvailable.value = null
  error.value = ''
  success.value = ''
}

async function confirmNickChange() {
  error.value = ''
  success.value = ''
  const newName = (tempNickname.value || '').trim()
  if (!newName) {
    error.value = '用户名不能为空'
    return
  }
  if (nickAvailable.value === false) {
    error.value = '用户名已被占用'
    return
  }
  const token = localStorage.getItem('token')
  if (!token) {
    error.value = '未登录'
    return
  }
  try {
    const res = await fetch('http://127.0.0.1:8000/users/me', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({username: newName})
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      error.value = data.detail || '更新失败'
      return
    }
    success.value = '用户名更新成功'
    username.value = newName
    user.username = newName
    editingNick.value = false
  } catch (_) {
    error.value = '网络错误'
  }
}

function onNickInput() {
  error.value = ''
  success.value = ''
  debouncedNickCheck(tempNickname.value.trim())
}

async function onSubmit() {
  if (editingNick.value) {
    await confirmNickChange()
  }
}

const goChangePassword = () => router.push('/change-password')
const logout = () => {
  user.logout()
  window.location.href = '/'
}

// --- avatar related (新增) ---
const avatarError = ref('')
const avatarSuccess = ref('')
const avatarInfo = ref('')
const previewAvatar = ref(null) // data URL for preview
const selectedBlob = ref(null) // Blob to upload

// compute current avatar shown: store.avatar (remote or data) > preview > generated default
function nameColorSeed(name) {
  let h = 0
  for (let i = 0; i < name.length; i++) {
    h = (h << 5) - h + name.charCodeAt(i)
    h |= 0
  }
  const r = (h & 0xff0000) >> 16
  const g = (h & 0x00ff00) >> 8
  const b = h & 0x0000ff
  return {r: (r + 200) % 256, g: (g + 120) % 256, b: (b + 40) % 256}
}

function generateColorAvatarDataUrl(name, size = 100) {
  const {r, g, b} = nameColorSeed(name || 'U')
  const canvas = document.createElement('canvas')
  canvas.width = size
  canvas.height = size
  const ctx = canvas.getContext('2d')
  ctx.fillStyle = `rgb(${r}, ${g}, ${b})`
  ctx.fillRect(0, 0, size, size)
  if (name && name.length) {
    const letter = name.trim()[0].toUpperCase()
    ctx.fillStyle = 'rgba(255,255,255,0.95)'
    ctx.font = `${Math.floor(size * 0.5)}px sans-serif`
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(letter, size / 2, size / 2)
  }
  return canvas.toDataURL('image/png')
}

const defaultAvatar = generateColorAvatarDataUrl(user.username || 'U', 100)
const currentAvatar = computed(() => {
  if (user.avatar) {
    // user.avatar is expected to be like "/user_images/user_1.png" or a full data URL
    if (user.avatar.startsWith('http') || user.avatar.startsWith('data:')) return user.avatar
    return `http://127.0.0.1:8000${user.avatar}`
  }
  if (previewAvatar.value) return previewAvatar.value
  return defaultAvatar
})

// handle file selection: validate square client-side, scale to 100x100 and keep blob
function onAvatarFileChange(e) {
  avatarError.value = ''
  avatarSuccess.value = ''
  avatarInfo.value = ''
  previewAvatar.value = null
  selectedBlob.value = null

  const file = e.target.files && e.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    avatarError.value = '请选择图片文件'
    return
  }

  const reader = new FileReader()
  reader.onload = () => {
    const img = new Image()
    img.onload = () => {
      if (img.width !== img.height) {
        avatarError.value = '上传图片必须为正方形（宽高 1:1）'
        return
      }
      // draw to 100x100 canvas
      const canvas = document.createElement('canvas')
      canvas.width = 100
      canvas.height = 100
      const ctx = canvas.getContext('2d')
      ctx.drawImage(img, 0, 0, 100, 100)
      canvas.toBlob((blob) => {
        if (!blob) {
          avatarError.value = '处理图片失败'
          return
        }
        selectedBlob.value = blob
        previewAvatar.value = canvas.toDataURL('image/png')
        avatarInfo.value = '已准备好上传'
      }, 'image/png')
    }
    img.onerror = () => {
      avatarError.value = '无法读取图片'
    }
    img.src = reader.result
  }
  reader.onerror = () => {
    avatarError.value = '读取文件失败'
  }
  reader.readAsDataURL(file)
}

function clearAvatarSelection() {
  previewAvatar.value = null
  selectedBlob.value = null
  avatarError.value = ''
  avatarSuccess.value = ''
  avatarInfo.value = ''
  // reset file input if needed by user manually
}

async function uploadAvatar() {
  avatarError.value = ''
  avatarSuccess.value = ''
  avatarInfo.value = ''

  if (!selectedBlob.value) {
    avatarError.value = '请先选择并确认一张正方形图片'
    return
  }
  const token = localStorage.getItem('token')
  if (!token) {
    avatarError.value = '未登录'
    return
  }
  const formData = new FormData()
  formData.append('file', selectedBlob.value, 'avatar.png')

  try {
    const res = await fetch('http://127.0.0.1:8000/users/me/avatar', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      avatarError.value = data.detail || '上传失败'
      return
    }
    const data = await res.json().catch(() => ({}))
    const url = data.url || null
    if (url) {
      // 使用后端返回的 URL（例如 /user_images/user_{id}.png）
      user.setAvatar(url)
      avatarSuccess.value = '上传成功'
      previewAvatar.value = null
      selectedBlob.value = null
    } else {
      // 后端未返回 url，使用本地 preview
      user.setAvatar(previewAvatar.value)
      avatarSuccess.value = '上传成功（本地预览）'
      previewAvatar.value = null
      selectedBlob.value = null
    }
  } catch (_) {
    avatarError.value = '网络错误'
  }
}
</script>

<style scoped>
.input_sml {
  @apply border border-gray-300 p-1 rounded bg-white text-gray-900;
}

.bt_sml_defa {
  @apply bg-gray-200 text-gray-800 py-1 px-3 rounded;
}
.bt_sml_defa_narr {
  @apply bg-gray-100 text-gray-800 py-1 px-3 rounded;
}
.bt_sml_main {
  @apply bg-blue-600 text-white py-1 px-3 rounded;
}

/* 确保头像 img 圆形 */
img {
  border-radius: 9999px;
  display: block;
}
</style>