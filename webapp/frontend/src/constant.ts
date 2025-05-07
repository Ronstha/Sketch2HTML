export const BACKEND_URL=`http://${window.location.hostname}:5000`
export const local_file=(path:string)=>{return BACKEND_URL+"/get_image"+path}