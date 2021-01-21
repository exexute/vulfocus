import request from '@/utils/request'

/**
 * 添加镜像
 * @param data 镜像信息
 * @constructor
 */
export function ImageAdd(data) {
  return request({
    url: '/images/',
    method: 'post',
    data
  })
}

/**
 * 更新镜像信息
 * @param id
 * @param data
 * @constructor
 */
export function ImageEdit(id, data) {
  return request({
    url: "/images/" + id + "/edit/",
    method: 'post',
    data
  })
}

/**
 * 删除镜像
 * @param id 镜像id
 * @constructor
 */
export function ImageDelete(id) {
  return request({
    url: '/images/' + id + '/delete/'
  })
}

/**
 * 加载本地镜像
 * @constructor
 */
export function ImageLocal() {
  return request({
    url: '/images/local/local/'
  })
}

/**
 * 添加本地镜像
 * @param data 镜像信息
 * @constructor
 */
export function ImageLocalAdd(data) {
  return request({
    url: '/images/local/local_add/',
    method: 'post',
    data
  })
}

/**
 * 停止下载镜像
 * @param id
 * @constructor
 */
export function ImageTaskTerminal(id) {
  return request({
    url: '/images/' + id + '/stop/',
    method: 'post',
  })
}

/**
 * 下载镜像
 * @param id
 * @constructor
 */
export function ImageDownload(id) {
  return request({
    url: '/images/' + id + '/download/'
  })
}


/**
 * 分享镜像
 * @param id 镜像 ID
 * @constructor
 */
export function ImageShare(id) {
  return request({
    url: '/images/' + id + '/share/'
  })
}

/**
 * 安装IAST
 * @param {*} baseImageName 
 * @param {*} imageName 
 * @param {*} ports 
 */
export function ImageInstallIast(baseImageName, imageName, ports) {
  return request({
    url: '/iast/autoBuild?baseImageName=' + baseImageName + '&imageName=' + imageName + '&ports=' + ports,
  })
}

/**
 * 重新安装IAST
 * @param {*} baseImageName 
 * @param {*} ports 
 */
export function ReImageInstallIast(baseImageName, ports) {
  return request({
    url: '/iast/rebuild?baseImageName=' + baseImageName + '&ports=' + ports,
  })
}