import request from '@/utils/request'

// 查询操作日志列表
export function list(query) {
  return request({
    url: '/monitor/operlog/',
    method: 'get',
    params: query
  })
}

// 删除操作日志
export function delOperlog(oper_id) {
  return request({
    url: `/monitor/operlog/${oper_id}/`,
    method: 'delete'
  })
}

// 清空操作日志
export function cleanOperlog() {
  return request({
    url: '/monitor/operlog/',
    method: 'delete'
  })
}
