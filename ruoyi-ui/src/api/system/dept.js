import request from '@/utils/request'

// 查询部门列表
export function listDept(query) {
  return request({
    url: '/system/dept/',
    method: 'get',
    params: query
  })
}

// 查询部门列表（排除节点）
export function listDeptExcludeChild(dept_id) {
  return request({
    url: `/system/dept/exclude/${dept_id}/`,
    method: 'get'
  })
}

// 查询部门详细
export function getDept(dept_id) {
  return request({
    url: `/system/dept/${dept_id}/`,
    method: 'get'
  })
}

// 查询部门下拉树结构
export function treeselect() {
  return request({
    url: '/system/dept/tree_select/',
    method: 'get'
  })
}

// 根据角色ID查询部门树结构
export function roleDeptTreeselect(role_id) {
  return request({
    url: `/system/dept/role_dept_tree_select/${role_id}/`,
    method: 'get'
  })
}

// 新增部门
export function addDept(data) {
  return request({
    url: '/system/dept/',
    method: 'post',
    data: data
  })
}

// 修改部门
export function updateDept(data) {
  return request({
    url: '/system/dept/',
    method: 'put',
    data: data
  })
}

// 删除部门
export function delDept(dept_id) {
  return request({
    url: `/system/dept/${dept_id}/`,
    method: 'delete'
  })
}
