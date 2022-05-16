document.addEventListener("DOMContentLoaded", () => {

  let url = window.location.pathname;
  console.log(url);

  if (url == "/") {
    document.querySelector("#editPosts").style.display = "none";
    let edits = document.querySelectorAll("#edit");

    createPost();

    edits.forEach(elemento => {
      elemento.addEventListener("click", () => {
        console.log("click   /");
        document.querySelector("#allPost").style.display = "none";
        document.querySelector("#formPost").style.display = "none";

        let idpost = elemento.getAttribute("value");
        editPost(idpost);

      })
    })

    const divs = document.querySelectorAll(".divPost");
    const hashCSRF = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    divs.forEach(item => {
      let heart = item.querySelector("img");
      let postid = item.querySelector("#idpost").innerText;
      let navbars = document.querySelectorAll(".nav-item");
      let currentUSer = navbars[0].querySelector(".nav-link").textContent;
      let clickedUser = item.querySelector("#user").textContent;

      if (currentUSer !== clickedUser) {
        heart.addEventListener("click", () => {

          async function heartGET() {
            const settingsGET = {
              method: "GET"
            }
            const response = await fetch(`/likedpost/${postid}`, settingsGET);
            const responseJSON = await response.json();
            return responseJSON
          }

          async function heartPOST() {
            const settingPOST = {
              method: "POST",
              headers: {
                "X-CSRFToken": hashCSRF
              },
              body: JSON.stringify({
                "ilike": 1,
                "idPost": postid
              })
            }
            const response = await fetch(`/likedpost/${postid}`, settingPOST);
            const responseJSON = await response.json();
            return responseJSON
          }

          async function heartPUT() {
            const settingsPUT = {
              method: "PUT",
              headers: {
                'X-CSRFToken': hashCSRF
              },
              body: JSON.stringify({
                "postid": postid,
              })
            }
            const response = await fetch(`/likedpost/${postid}`, settingsPUT);
            const responseJSON = await response.json();
            return responseJSON
          }

          heartGET().then(response => {
            console.log(response.data[0]);
            if (response.data[0] == "yes") {
              heartPUT().then(responsePut => {
                console.log(responsePut);
                window.location.reload();
              })
            } else if (response.data[0] == "no") {
              heartPOST().then(responsePOST => {
                console.log(responsePOST);
                window.location.reload();
              })
            }
          })
        })
      }
    })

  } else if (url == "/posts") {
    let edits = document.querySelectorAll("#edit");
    document.querySelector("#editPosts").style.display = "none";
    edits.forEach(elemento => {
      elemento.addEventListener("click", () => {
        console.log("click   /posts");
        document.querySelector("#editPosts").style.display = "block";
        document.querySelector("#userPost").style.display = "none";

        let idpost = elemento.getAttribute("value");
        editPost(idpost);

      })
    })
  } else if (url == "/following") {
    let divsposts = document.querySelectorAll(".postFollowing");
    divsposts.forEach(elemento => {
      elemento.querySelector("#heart").addEventListener("click", () => {
        console.log("click   /following");
        let postid = elemento.querySelector("#heart").getAttribute("value");

        let cookiehashCSRF = document.cookie.split("=")[1].toString()

        async function heartGET() {
          const settingsGET = {
            method: "GET"
          }
          const response = await fetch(`/likedpost/${postid}`, settingsGET);
          const responseJSON = await response.json();
          return responseJSON
        }

        async function heartPOST() {
          const settingPOST = {
            method: "POST",
            headers: {
              "X-CSRFToken": cookiehashCSRF
            },
            body: JSON.stringify({
              "ilike": 1,
              "idPost": postid
            })
          }
          const response = await fetch(`/likedpost/${postid}`, settingPOST);
          const responseJSON = await response.json();
          return responseJSON
        }

        async function heartPUT() {
          const settingsPUT = {
            method: "PUT",
            headers: {
              'X-CSRFToken': cookiehashCSRF
            },
            body: JSON.stringify({
              "postid": postid,
            })
          }
          const response = await fetch(`/likedpost/${postid}`, settingsPUT);
          const responseJSON = await response.json();
          return responseJSON
        }

        heartGET().then(response => {
          console.log(response.data[0]);
          if (response.data[0] == "yes") {
            heartPUT().then(responsePut => {
              console.log(responsePut);
              window.location.reload()
            })
          } else if (response.data[0] == "no") {
            heartPOST().then(responsePOST => {
              console.log(responsePOST);
              window.location.reload()
            })
          }
        })
      })
    })
    ////////////////////////////////////
    ////////////////////////////////////
  } else if (url.search("/userview/") === 0) {
    let buttonfollow = document.querySelector("#follow");
    buttonfollow.addEventListener("click", () => {
      console.log("click");
      let userFollow = buttonfollow.getAttribute("value");

      let cookiehashCSRF = document.cookie;

      async function getFollow() {
        const methodSettings = {
          method: "GET"
        }
        const respuesta = await fetch(`/createFollowing/${userFollow}`, methodSettings);
        const respuestaJSON = await respuesta.json();
        return respuestaJSON
      }

      async function postFollow() {
      	const postFollowSettings = {
      	  method: "POST",
      	  headers: {
      	    "X-CSRFToken": cookiehashCSRF.split("=")[1].toString()
      	  },
      	  body: JSON.stringify({
      	    "userToFollow": userFollow
      	  })
      	}
      	const respuesta = await fetch(`/createFollowing/${userFollow}`, postFollowSettings);
      	const respuestaJSON = await respuesta.json();
      	return respuestaJSON
      }

      async function putFollow() {
        const putSettings = {
          method: "PUT",
          headers: {
            "X-CSRFToken": cookiehashCSRF.split("=")[1].toString()
          },
          body: JSON.stringify({
            "userFollowing": userFollow,
            "delete": "yes"
          })
        }
        const response = await fetch(`/createFollowing/${userFollow}`, putSettings);
        const responseJSON = await response.json();
        return responseJSON
      }

      getFollow().then(respuesta => {
        if (respuesta.ifollow == "no") {
          postFollow().then(response => {
              console.log(response);
              // document.querySelector("#follow").innerText = "following"
              window.location.reload();
            })
        } else if (respuesta.ifollow == "yes") {
          putFollow().then(respuesta => {
            console.log(respuesta);
            // document.querySelector("#follow").innerText = "follow"
            window.location.reload();
          })
        }
      })
    });
    let divPost = document.querySelectorAll(".divPost");
    divPost.forEach(elemento => {
      elemento.querySelector("#heart").addEventListener("click", () => {
        let postid = elemento.querySelector("#idpost").innerText;
        console.log("click", idpost);
        let cookiehashCSRF = document.cookie.split("=")[1].toString()

        async function heartGET() {
          const settingsGET = {
            method: "GET"
          }
          const response = await fetch(`/likedpost/${postid}`, settingsGET);
          const responseJSON = await response.json();
          return responseJSON
        }

        async function heartPOST() {
          const settingPOST = {
            method: "POST",
            headers: {
              "X-CSRFToken": cookiehashCSRF
            },
            body: JSON.stringify({
              "ilike": 1,
              "idPost": postid
            })
          }
          const response = await fetch(`/likedpost/${postid}`, settingPOST);
          const responseJSON = await response.json();
          return responseJSON
        }

        async function heartPUT() {
          const settingsPUT = {
            method: "PUT",
            headers: {
              'X-CSRFToken': cookiehashCSRF
            },
            body: JSON.stringify({
              "postid": postid,
            })
          }
          const response = await fetch(`/likedpost/${postid}`, settingsPUT);
          const responseJSON = await response.json();
          return responseJSON
        }

        heartGET().then(response => {
          console.log(response.data[0]);
          if (response.data[0] == "yes") {
            heartPUT().then(responsePut => {
              console.log(responsePut);
              window.location.reload()
            })
          } else if (response.data[0] == "no") {
            heartPOST().then(responsePOST => {
              console.log(responsePOST);
              window.location.reload()
            })
          }
        })
      })
    })


  }

});


function editPost(idPost) {
  let h3 = document.querySelector("h3");
  h3.innerHTML = "";
  h3.innerText = "Editing Post";
  document.querySelector("#editPosts").style.display = "flex";
  const hashCSRF = document.querySelector("#formEdit").querySelector('[name="csrfmiddlewaretoken"]').value;
  let textarea = document.querySelector("#editPost");
  const formularioPOST = document.querySelector(`#editPosts`);

  async function posTGET() {
    const getSettings = {
      method: "GET"
    }
    const response = await fetch(`/postedit/${idPost}`, getSettings);
    const responseJSON = await response.json();
    return responseJSON
  }

  async function postPUT() {
    const settingsPUT = {
      method: "PUT",
      headers: {
        'X-CSRFToken': hashCSRF
      },
      body: JSON.stringify({
        "data": textarea.value,
        "postid": idPost,
      })
    }
    const response = await fetch(`/postedit/${idPost}`, settingsPUT);
    const responseJSON = await response.json();
    return responseJSON
  }


  posTGET().then(response => {
    console.log(response);
    let textarea = document.querySelector("#editPost");
    textarea.value = response.postText;
    formularioPOST.onsubmit = (evento) => {
      evento.preventDefault();
      postPUT().then(respuesta => {
        console.log(respuesta);
        textarea.value = "";
        if (window.location.pathname == "/") {
          window.location.href = "/"
        } else if (window.location.pathname == "/posts") {
          window.location.href = "/posts";
        }
      })
    }
  })
}


function createPost() {
  let formularioPOST = document.querySelector("#formPost");
  formularioPOST.style.display = "flex";
  formularioPOST.onsubmit = (evento) => {
    evento.preventDefault();

    let text = document.querySelector("#id_newPost");

    const hashCSRF = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    const meses = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const date = new Date();
    let segundos = "";
    let minutos = "";
    if (date.getSeconds() < 10) {
      segundos = `0${date.getSeconds()}`;
    } else {
      segundos = `${date.getSeconds()}`;
    }
    if (date.getMinutes() < 10) {
      minutos = `0${date.getMinutes()}`;
    } else {
      minutos = `${date.getMinutes()}`;
    }
    const fecha = `${meses[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}, ${date.getHours()}:${minutos}:${segundos}`;
    fetch("/createpost", {
      method: "POST",
      headers: {
        'X-CSRFToken': hashCSRF
      },
      body: JSON.stringify({
        "text": text.value,
        "date": fecha,
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log(data.message);
      text.value = "";
      window.location.href = "/";
    })
    .catch(error => {
      console.log(error);
    });
  }
}
