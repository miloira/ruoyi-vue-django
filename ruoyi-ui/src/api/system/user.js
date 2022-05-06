import request from '@/utils/request'
import { parseStrEmpty } from "@/utils/ruoyi";

// 查询用户列表
export function listUser(query) {
  return request({
    url: '/system/user/',
    method: 'get',
    params: query
  })
}

// 查询用户详细
export function getUser(user_id) {
  return request({
    url: `/system/user/${user_id}/`,
    method: 'get'
  })
}

// 添加用户的选项
export function getUserOptions() {
  return request({
    url: '/system/user/option/',
    method: 'get'
  })
}

// 新增用户
export function addUser(data) {
  return request({
    url: '/system/user/',
    method: 'post',
    data: data
  })
}

// 修改用户
export function updateUser(data) {
  return request({
    url: '/system/user/',
    method: 'put',
    data: data
  })
}

// 删除用户
export function delUser(user_id) {
  return request({
    url: `/system/user/${user_id}/`,
    method: 'delete'
  })
}

// 用户密码重置
export function resetUserPwd(user_id, password) {
  const data = {
    user_id,
    password
  }
  return request({
    url: '/system/user/reset_pwd/',
    method: 'put',
    data: data
  })
}

// 用户状态修改
export function changeUserStatus(user_id, status) {
  const data = {
    user_id,
    status
  }
  return request({
    url: '/system/user/change_status/',
    method: 'put',
    data: data
  })
}

// 查询用户个人信息
export function getUserProfile() {
  return request({
    url: '/system/user/profile/',
    method: 'get'
  })
}

// 修改用户个人信息
export function updateUserProfile(data) {
  return request({
    url: '/system/user/profile/',
    method: 'put',
    data: data
  })
}

// 用户密码重置
export function updateUserPwd(old_password, new_password) {
  const data = {
    old_password,
    new_password
  }
  return request({
    url: '/system/user/profile/update_pwd/',
    method: 'put',
    data: data
  })
}

// 用户头像上传
export function uploadAvatar(data) {
  return request({
    url: '/system/user/profile/avatar/',
    method: 'post',
    data: data
  })
}

// 查询授权角色
export function getAuthRole(user_id) {
  return request({
    url: `/system/user/auth_role/${user_id}/`,
    method: 'get'
  })
}

// 保存授权角色
export function updateAuthRole(user_id, data) {
  return request({
    url: `/system/user/auth_role/${user_id}/`,
    method: 'put',
    data: data
  })
}
