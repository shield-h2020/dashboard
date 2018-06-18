export function ipValidator(ip) {
  if (!ip || typeof ip !== 'string') return false;

  const regex = new RegExp(/^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/);
  return regex.test(ip);
}

export default {
  ipValidator,
};
