import request from '@/utils/request'

// 查询菜单列表
export function listMenu(query) {
  return request({
    url: '/system/menu/',
    method: 'get',
    params: query
  })
}

// 查询菜单详细
export function getMenu(menu_id) {
  return request({
    url: `/system/menu/${menu_id}/`,
    method: 'get'
  })
}

// 查询菜单下拉树结构
export function treeselect() {
  return request({
    url: '/system/menu/tree_select/',
    method: 'get'
  })
}

// 根据角色ID查询菜单下拉树结构
export function roleMenuTreeselect(role_id) {
  return request({
    url: `/system/menu/role_menu_tree_select/${role_id}/`,
    method: 'get'
  })
}

// 新增菜单
export function addMenu(data) {
  return request({
    url: '/system/menu/',
    method: 'post',
    data: data
  })
}

// 修改菜单
export function updateMenu(data) {
  return request({
    url: '/system/menu/',
    method: 'put',
    data: data
  })
}

// 删除菜单
export function delMenu(menu_id) {
  return request({
    url: `/system/menu/${menu_id}/`,
    method: 'delete'
  })
}
