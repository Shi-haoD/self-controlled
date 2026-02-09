import { requestClient } from '#/api/request';

/**
 * 获取系统支持的时区列表
 */
export async function getTimezoneOptionsApi() {
  return await requestClient.get<
    {
      label: string;
      value: string;
    }[]
  >('/v1/timezone/getTimezoneOptions');
}
/**
 * 获取用户时区
 */
export async function getTimezoneApi(): Promise<null | string | undefined> {
  return requestClient.get<null | string | undefined>('/v1/timezone/getTimezone');
}
/**
 * 设置用户时区
 * @param timezone 时区
 */
export async function setTimezoneApi(timezone: string): Promise<void> {
  return requestClient.post('/v1/timezone/setTimezone', { timezone });
}
