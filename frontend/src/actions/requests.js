import config from '../config'

function status(response){
  if(response.ok){
    return response.json()
  } else {
    let error = new Error(response.statusText || response.status )
    error.response = response
    throw error
  }
}

export function requestYoutubeTrack(youtube_id, comment){
  const data = { youtube_id, comment }
  return fetch(
    config.apiServer + '/api/add/from/youtube', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      }
  }).then(status)
}

export function requestFileTrack(formData){
  return fetch(
    config.apiServer + '/api/add/from/file', {
      method: 'POST',
      mode: 'cors',
      body: formData,
      headers: {
        /* 'Content-Type': 'multipart/form-data',*/
      }
    }
  ).then(status)
}
