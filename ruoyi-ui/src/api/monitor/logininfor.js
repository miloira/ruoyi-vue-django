import request from '@/utils/request'

// 查询登录日志列表
export function list(query) {
  return request({
    url: '/monitor/logininfor/',
    method: 'get',
    params: query
  })
}

// 删除登录日志
export function delLogininfor(info_id) {
  return request({
    url: `/monitor/logininfor/${info_id}/`,
    method: 'delete'
  })
}

// 清空登录日志
export function cleanLogininfor() {
  return request({
    url: '/monitor/logininfor/',
    method: 'delete'
  })
}
