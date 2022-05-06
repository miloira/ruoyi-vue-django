import request from '@/utils/request'

// 查询角色列表
export function listRole(query) {
  return request({
    url: '/system/role/',
    method: 'get',
    params: query
  })
}

// 查询角色详细
export function getRole(role_id) {
  return request({
    url: `/system/role/${role_id}/`,
    method: 'get'
  })
}

// 新增角色
export function addRole(data) {
  return request({
    url: '/system/role/',
    method: 'post',
    data: data
  })
}

// 修改角色
export function updateRole(data) {
  return request({
    url: '/system/role/',
    method: 'put',
    data: data
  })
}

// 角色数据权限
export function dataScope(data) {
  return request({
    url: '/system/role/data_scope/',
    method: 'put',
    data: data
  })
}

// 角色状态修改
export function changeRoleStatus(role_id, status) {
  const data = {
    role_id,
    status
  }
  return request({
    url: '/system/role/change_status/',
    method: 'put',
    data: data
  })
}

// 删除角色
export function delRole(role_id) {
  return request({
    url: `/system/role/${role_id}/`,
    method: 'delete'
  })
}

// 查询角色已授权用户列表
export function allocatedUserList(query) {
  return request({
    url: '/system/role/auth_user/allocated_list/',
    method: 'get',
    params: query
  })
}

// 查询角色未授权用户列表
export function unallocatedUserList(query) {
  return request({
    url: '/system/role/auth_user/unallocated_list/',
    method: 'get',
    params: query
  })
}

// 取消用户授权角色
export function authUserCancel(data) {
  return request({
    url: '/system/role/auth_user/cancel/',
    method: 'put',
    data: data
  })
}

// 批量取消用户授权角色
export function authUserCancelAll(data) {
  return request({
    url: '/system/role/auth_user/cancel_all/',
    method: 'put',
    params: data
  })
}

// 授权用户选择
export function authUserSelectAll(data) {
  return request({
    url: '/system/role/auth_user/select_all/',
    method: 'put',
    params: data
  })
}
