import request from '@/utils/request'

// 查询字典数据列表
export function listData(query) {
  return request({
    url: '/system/dict/data/',
    method: 'get',
    params: query
  })
}

// 查询字典数据详细
export function getData(dict_code) {
  return request({
    url: `/system/dict/data/${dict_code}/`,
    method: 'get'
  })
}

// 根据字典类型查询字典数据信息
export function getDicts(dict_type) {
  return request({
    url: `/system/dict/data/type/${dict_type}/`,
    method: 'get'
  })
}

// 新增字典数据
export function addData(data) {
  return request({
    url: '/system/dict/data/',
    method: 'post',
    data: data
  })
}

// 修改字典数据
export function updateData(data) {
  return request({
    url: '/system/dict/data/',
    method: 'put',
    data: data
  })
}

// 删除字典数据
export function delData(dict_code) {
  return request({
    url: `/system/dict/data/${dict_code}/`,
    method: 'delete'
  })
}
