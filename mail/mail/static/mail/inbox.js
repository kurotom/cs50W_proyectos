document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);


  document.querySelector("#compose-recipients").addEventListener("click", () => {
    if (document.querySelector("#compose-recipients").value != "") {

      let recipientString = document.querySelector("#compose-recipients").value;

      let userErrorMail = document.querySelector("#errorUser").textContent;

      const re = /\S+@\S+\.\S+/gi;
      userErrorMail = document.querySelector("#errorUser").textContent;
      let borrar = userErrorMail.match(re)[0];

      let newValue = recipientString.slice((borrar.length), recipientString.length);
      console.log(newValue);

      document.querySelector("#compose-recipients").value = newValue;

      var parentCompose = document.getElementsByClassName("form-group")[1];
      var pAviso = parentCompose.querySelector("p");

      let allTagP = document.getElementsByClassName("form-group")[1].querySelectorAll("p")
      console.log(allTagP);
      allTagP.forEach(elemento => parentCompose.removeChild(elemento))

    } else {
      document.querySelector("#compose-recipients").value = "";
      var parentCompose = document.getElementsByClassName("form-group")[1];
      var pAviso = parentCompose.querySelector("p");

      let allTagP = document.getElementsByClassName("form-group")[1].querySelectorAll("p")
      allTagP.forEach(elemento => parentCompose.removeChild(elemento))
    }
  });


  let compose_subject = document.querySelector("#compose-subject");
  compose_subject.addEventListener("click", () => {
    if (compose_subject.value == "") {
      console.log(`Subject Vacio`);
      var parentCompose = document.getElementsByClassName("form-group")[2];
      var pAviso = parentCompose.querySelector("p");

      let allTagP = document.getElementsByClassName("form-group")[2].querySelectorAll("p")
      allTagP.forEach(elemento => parentCompose.removeChild(elemento))

    }
  });

  document.querySelector("#compose-body").addEventListener("click", () => {
    if (document.querySelector("#compose-body").value == "") {
      console.log("Compose VACIO");
      console.log(document.querySelector("#compose-body").value);

    }
  });

  // By default, load the inbox
  load_mailbox('inbox');
});




function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#ArchivedMail').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  const formaularioReply = document.querySelector("#compose-form");
  formaularioReply.onsubmit = (evento) => {
    evento.preventDefault();
    const recipients = document.querySelector("#compose-recipients").value.split(",");
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;

    if (recipients != [] && subject != "" && body != "") {

      let users = [];
      recipients.forEach(person => {
        users.push(person.trim());
      });
      fetch("/emails", {
        method: "POST",
        body: JSON.stringify({
          recipients: users.toString(),
          subject: subject,
          body: body
        })
      })
      .then(response => {
        return response.json();
      })
      .then(data => {
        if (data.message != "Email sent successfully.") {
          var elementoP = document.createElement("p");
          var dataElementP = document.createTextNode(data.error);
          elementoP.appendChild(dataElementP);
          let ErrorMailDontExists = document.getElementsByClassName("form-group")[1].appendChild(elementoP);
          ErrorMailDontExists.setAttribute("id", "errorUser");

          document.getElementById("errorUser").style.cssText = `
          display: flex;
          justify-content: center;
          font-weight: bold;
          `;

          window.scrollTo({top: 60, behavior: "smooth"});

        } else {
          console.log("EXITO");
          load_mailbox("sent");
        }
      })
      .catch(error => {
        console.log(response.error);
        console.log(error);
      });
    }
  }
}



function replyMail() {
  document.querySelector('#emails-view').style.display = "none";
  document.querySelector("#emailOpenView").style.display = "none";
  document.querySelector("#ArchivedMail").style.display = "none";
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#compose-view').querySelector("h3").innerHTML = "Reply Email";

  let subjectAntiguo = ``;
  let subject = document.querySelector("#emailOpenView").querySelector("#subject").querySelector("strong").textContent;
  let bodyP = document.querySelector("#emailOpenView").querySelector("#body").innerHTML;
  let timestamp = document.querySelector("#emailOpenView").querySelector("#timestamp").textContent;
  let sender = document.querySelector("#emailOpenView").querySelector("#sender").querySelector("strong").textContent;
  let recipients = document.querySelector("#emailOpenView").querySelector("#recipients").querySelector("strong").textContent;
  let mailID = document.querySelector("#emailOpenView").querySelector("#id").textContent;

  const regx = /Re:/g;
  if (regx.test(subject) === false) {
    console.log("1", subject, `Re: ${subject}`);
    document.querySelector("#compose-subject").value = `Re: ${subject}`;
    subjectAntiguo = `Re: ${subject}`;
  } else {
    subjectAntiguo = subject;
  }

  document.querySelector("#compose-recipients").value = sender;
  document.querySelector("#compose-subject").value = subjectAntiguo;
  document.querySelector("#compose-body").value =
  "\n" +
  "\n----------------------------------------\n" +
  "----------------------------------------\n" +
  "On "+ timestamp + " " + sender + " wrote: \n" +
  bodyP.replaceAll("<br>", "\n") +
  "\n"
  ;

  const formaularioReply = document.querySelector("#compose-form");
  formaularioReply.onsubmit = (evento) => {
    evento.preventDefault();
    let newbody = document.querySelector("#compose-body").value;

    fetch("/emails", {
      method: "POST",
      body: JSON.stringify({
        recipients: sender,
        subject: subjectAntiguo,
        body: newbody
      })
    })
    .then(response => response.json())
    .then(data => {
      document.querySelector('#emails-view').style.cssText = `
      display: flex;
      flex-direction: column;
      flex-wrap: wrap;
      align-items: center;
      `;
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector("#emailOpenView").style.display = "none";
      document.querySelector("#ArchivedMail").style.display = "none";
      load_mailbox("inbox");
    })
    .catch(error => console.log(error));
    load_mailbox("inbox");
  }
}






function load_mailbox(mailbox) {
  console.log(`Inicio FUNCION MAILBOX --> ${mailbox}`);
//
//
//                  INBOX
  if (mailbox == "inbox") {

    document.querySelector('#emails-view').style.cssText = `
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    align-items: center;
    `;
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector("#emailOpenView").style.display = "none";
    document.querySelector("#ArchivedMail").style.display = "none";

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    console.log(">>>> INBOX");

    fetch(`/emails/${mailbox}`, {method: "GET"})
    .then(response => response.json())
    .then(data => {
      data.forEach(elemento => {
        let contentMail = "";
        if (mailbox == "inbox") {
          contentMail = `
          <span>Sender: <strong>${elemento.sender}</strong></span>
          <br>
          <span>Subject: <strong>${elemento.subject.slice(0, 10)} ...</strong></span>
          <br>
          <span>${elemento.timestamp}</span>
          <br>
          <span class="hide">${elemento.id}</span>
          `;
        }

        let parent = document.querySelector('#emails-view');
        let sondiv = document.createElement("div");
        sondiv.setAttribute("class", "divMailContent");

        let colorBackground = "";
        if (elemento.read == true) {
          sondiv.style.cssText = `
          background-color: grey;
          margin-bottom: 20px;
          border: 1px solid black;
          padding: 10px;
          width: 70%;
          display: flex;
          justify-content: center;
          flex-direction: row;
          gap: 5%;
          `;
        } else {
          sondiv.style.cssText = `
          background-color: white;
          margin-bottom: 20px;
          border: 1px solid black;
          padding: 10px;
          width: 70%;
          display: flex;
          justify-content: center;
          flex-direction: row;
          gap: 5%;
          `;
        }

        sondiv.innerHTML = contentMail;
        parent.appendChild(sondiv);

        let hideIDclass = document.querySelectorAll(".hide");
        hideIDclass.forEach(item => item.style.display = "none");

      })
    })
    .then(ele => {
      let divMail = document.querySelectorAll(".divMailContent");
      divMail.forEach(item => {
        item.addEventListener("click", () => {
          let idMail = item.querySelector(".hide").textContent;

          fetch(`/emails/${idMail}`, {method: "GET"})
          .then(response => response.json())
          .then(data => {

            console.log("PUT READ");

            fetch(`/emails/${idMail}`, {
              method: "PUT",
              body: JSON.stringify({
                read: true
              })
            })

            document.querySelector('#ArchivedMail').style.display = "none";
            document.querySelector('#emails-view').style.display = "none";
            document.querySelector('#compose-view').style.display = 'none';
            const div = document.querySelector("#emailOpenView");
            div.style.display = "block";

            console.log(`Inbox - Fetch -> ele`);

            let contentMail = `
            <div id="contentMailUser">
              <span id="sender">Sender: <strong>${data.sender}</strong></span>
              <br>
              <span id="recipients">Recipient: <strong>${data.recipients}</strong></span>
              <br>
              <span id="timestamp">${data.timestamp}</span>

              <hr>
              <div>
                <button id="archive">Not archived</button>
                <button id="reply">Reply</button>
              </div>
              <span id="subject">Subject: <strong>${data.subject}</strong></span>
              <span>Body:</span>
              <p id="body"></p>
              <span id="id" style="display: none;">${idMail}</span>
            </div>
            `;

            div.innerHTML = contentMail;
            document.querySelector("#emailOpenView").querySelector("#body").innerHTML = data.body.replaceAll("\n", "<br>");

            document.querySelector("#contentMailUser").style.cssText = `
            display: flex;
            flex-direction: column;
            border: 1px solid black;
            padding: 20px;
            align-items: center;
            `

            let buttonHome = document.createElement("button");
            let parentDiv = document.querySelector("#emailOpenView");
            buttonHome.innerHTML = "Back";
            buttonHome.setAttribute("id", "buttonHome");
            parentDiv.appendChild(buttonHome);

          })
          .then(segundo => {
            console.log("inbox - Then Segundo");

            document.querySelector("#buttonHome").addEventListener("click", () => {
              document.querySelector('#emails-view').style.cssText = `
              display: flex;
              flex-direction: column;
              flex-wrap: wrap;
              align-items: center;
              `;
              document.querySelector('#compose-view').style.display = 'none';
              const div = document.querySelector("#emailOpenView");
              div.style.display = "none";
              load_mailbox("inbox");
            });
          })
          .then(archived => {
            console.log("inbox -> Then ARCHIVED ");
            document.querySelector("#archive").addEventListener("click", () => {
              console.log("PUSH ARCHIVED", idMail)
              fetch(`/emails/${idMail}`, {
                method: "PUT",
                body: JSON.stringify({
                  archived: true
                })
              })

              document.querySelector('#emails-view').style.cssText = `
              display: flex;
              flex-direction: column;
              flex-wrap: wrap;
              align-items: center;
              `;
              document.querySelector('#compose-view').style.display = 'none';
              document.querySelector("#emailOpenView").style.display = "none";
              document.querySelector("#ArchivedMail").style.display = "none";

              // Show the mailbox name
              document.querySelector('#ArchivedMail').innerHTML = `<h3>${"Archive".charAt(0).toUpperCase() + "Archive".slice(1)}</h3>`;

              load_mailbox("inbox");

            })
          })
          .then(reply => {
            document.querySelector("#reply").addEventListener("click", () =>  {
              console.log("inbox CLICK --> reply");

              fetch(`/emails/${idMail}`, {
                method: "PUT",
                body: JSON.stringify({
                  read: true
                })
              });

              replyMail();

            });
          })
          .catch(error => console.log(error));
        });
      })
    })
    .catch(error => console.log(error));
  }
//
//
//
//      SENT
//
  else if (mailbox == "sent") {
    document.querySelector('#emails-view').style.cssText = `
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    align-items: center;
    `;
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector("#emailOpenView").style.display = "none";
    document.querySelector("#ArchivedMail").style.display = "none";

    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch(`/emails/${mailbox}`, {method: "GET"})
    .then(response => response.json())
    .then(sentThen1 => {
      sentThen1.forEach(elemento => {
        let contentMail = "";
        if (mailbox == "sent") {
          contentMail = `
          <span>Recipient: <strong>${elemento.recipients}</strong></span>
          <br>
          <span>Subject: <strong>${elemento.subject.slice(0, 10)} ...</strong></span>
          <br>
          <span>${elemento.timestamp}</span>
          <br>
          <span class="hide">${elemento.id}</span>
          `;
        }
        let parent = document.querySelector('#emails-view');
        let sondiv = document.createElement("div");
        sondiv.setAttribute("class", "divMailContent");

        let colorBackground = "";
        if (elemento.read == true) {
          sondiv.style.cssText = `
          background-color: grey;
          margin-bottom: 20px;
          border: 1px solid black;
          padding: 10px;
          width: 70%;
          display: flex;
          justify-content: center;
          flex-direction: row;
          gap: 5%;
          `;
        } else {
          sondiv.style.cssText = `
          background-color: white;
          margin-bottom: 20px;
          border: 1px solid black;
          padding: 10px;
          width: 70%;
          display: flex;
          justify-content: center;
          flex-direction: row;
          gap: 5%;
          `;
        }
        sondiv.innerHTML = contentMail;
        parent.appendChild(sondiv);

        let hideIDclass = document.querySelectorAll(".hide");
        hideIDclass.forEach(item => item.style.display = "none");
      })
    })
    .then(then3Sent => {
      let divMail = document.querySelectorAll(".divMailContent");
      divMail.forEach(item => {
        item.addEventListener("click", () => {
          let idMail = item.querySelector(".hide").textContent;

          fetch(`/emails/${idMail}`, {method: "GET"})
          .then(response => response.json())
          .then(data => {

            fetch(`/emails/${idMail}`, {
              method: "PUT",
              body: JSON.stringify({
                read: true
              })
            })

            document.querySelector('#ArchivedMail').style.display = "none";
            document.querySelector('#emails-view').style.display = "none";
            document.querySelector('#compose-view').style.display = 'none';
            const div = document.querySelector("#emailOpenView");
            div.style.display = "block";

            let contentMail = `
            <div id="contentMailUser">
              <span id="sender">Sender: <strong>${data.sender}</strong></span>
              <br>
              <span id="recipients">Recipient: <strong>${data.recipients}</strong></span>
              <br>
              <span id="timestamp">${data.timestamp}</span>

              <hr>
              <span id="subject">Subject: <strong>${data.subject}</strong></span>
              <span>Body:</span>
              <p id="body"></p>
              <span id="id" style="display: none;">${idMail}</span>
            </div>
            `;

            div.innerHTML = contentMail;
            document.querySelector("#emailOpenView").querySelector("#body").innerText = data.body;

            document.querySelector("#contentMailUser").style.cssText = `
            display: flex;
            flex-direction: column;
            border: 1px solid black;
            padding: 20px;
            align-items: center;
            `

            let buttonHome = document.createElement("button");
            let parentDiv = document.querySelector("#emailOpenView");
            buttonHome.innerHTML = "Back";
            buttonHome.setAttribute("id", "buttonHome");
            parentDiv.appendChild(buttonHome);

          })
          .then(then4Sent => {
            console.log("sent 4");

            document.querySelector("#buttonHome").addEventListener("click", () => {
              document.querySelector('#emails-view').style.cssText = `
              display: flex;
              flex-direction: column;
              flex-wrap: wrap;
              align-items: center;
              `;
              document.querySelector('#compose-view').style.display = 'none';
              const div = document.querySelector("#emailOpenView");
              div.style.display = "none";
            });
          })
          .catch(error => console.log(error));
        })
      })
    })
    .catch(error => console.log(error));
  }

  //
  //      Archive
  //
  else if (mailbox == "archive") {
    document.querySelector('#ArchivedMail').style.cssText = `
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    align-items: center;
    `;
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector("#emailOpenView").style.display = "none";
    document.querySelector("#emails-view").style.display = "none";

    // Show the mailbox name
    document.querySelector('#ArchivedMail').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    console.log("if archived");

    fetch(`/emails/${mailbox}`, {method: "GET"})
    .then(response => response.json())
    .then(data => {
      console.log("Then 2 DATA Archive");
      data.forEach(elemento => {

        let parent = document.querySelector('#ArchivedMail');
        let sondiv = document.createElement("div");
        sondiv.setAttribute("class", "divMailContent");

        let contentMail = "";
        if (mailbox == "archive") {
          contentMail = `
          <span>Sender: <strong>${elemento.sender}</strong></span>
          <br>
          <span>Subject: <strong>${elemento.subject.slice(0, 10)} ...</strong></span>
          <br>
          <span>${elemento.timestamp}</span>
          <br>
          <span class="hide">${elemento.id}</span>
          `;
        }

        let colorBackground = "";
        if (elemento.read == true) {
          sondiv.style.cssText = `
          background-color: grey;
          margin-bottom: 20px;
          border: 1px solid black;
          padding: 10px;
          width: 70%;
          display: flex;
          justify-content: center;
          flex-direction: row;
          gap: 5%;
          `;
        } else {
          sondiv.style.cssText = `
          background-color: white;
          margin-bottom: 20px;
          border: 1px solid black;
          padding: 10px;
          width: 70%;
          display: flex;
          justify-content: center;
          flex-direction: row;
          gap: 5%;
          `;
        }

        sondiv.innerHTML = contentMail;
        parent.appendChild(sondiv);

        let hideIDclass = document.querySelectorAll(".hide");
        hideIDclass.forEach(item => item.style.display = "none");

      })
    })
    .then(then2Archive => {
      console.log("Then 2 Archive Open MAIL");
      let divMail = document.querySelectorAll(".divMailContent");
      divMail.forEach(item => {
        item.addEventListener("click", () => {
          let idMail = item.querySelector(".hide").textContent;

          fetch(`/emails/${idMail}`, {method: "GET"})
          .then(response => response.json())
          .then(data => {
            document.querySelector('#ArchivedMail').style.display = "none";
            document.querySelector('#emails-view').style.display = "none";
            document.querySelector('#compose-view').style.display = 'none';
            const div = document.querySelector("#emailOpenView");
            div.style.display = "block";

            let contentMail = `
            <div id="contentMailUser">
              <span id="sender">Sender: <strong>${data.sender}</strong></span>
              <br>
              <span id="recipients">Recipient: <strong>${data.recipients}</strong></span>
              <br>
              <span id="timestamp">${data.timestamp}</span>

              <hr>
              <div>
                <button id="archive">Archived</button>
                <button id="reply">Reply</button>
              </div>
              <span id="subject">Subject: <strong>${data.subject}</strong></span>
              <span>Body:</span>
              <p id="body"></p>
              <span id="id" style="display: none;">${idMail}</span>
            </div>
            `;

            div.innerHTML = contentMail;
            document.querySelector("#emailOpenView").querySelector("#body").innerText = data.body;

            document.querySelector("#contentMailUser").style.cssText = `
            display: flex;
            flex-direction: column;
            border: 1px solid black;
            padding: 20px;
            align-items: center;
            `
            fetch(`/emails/${idMail}`, {
              method: "PUT",
              body: JSON.stringify({
                read: true
              })
            })

            let buttonHome = document.createElement("button");
            let parentDiv = document.querySelector("#emailOpenView");
            buttonHome.innerHTML = "Back";
            buttonHome.setAttribute("id", "buttonHome");
            parentDiv.appendChild(buttonHome);
          })

          .then(OpenMailArchived => {
            console.log("THen 2 OpenMailArchived")

            document.querySelector("#buttonHome").addEventListener("click", () => {

              console.log("CLICK");

              document.querySelector('#ArchivedMail').style.cssText = `
              display: flex;
              flex-direction: column;
              flex-wrap: wrap;
              align-items: center;
              `;
              document.querySelector('#compose-view').style.display = 'none';
              const div = document.querySelector("#emailOpenView");
              div.style.display = "none";
            });
          })
          .then(archived => {
            console.log("Then ARCHIVED");
            document.querySelector("#archive").addEventListener("click", () => {
              console.log("PUSH ARCHIVED", idMail)
              fetch(`/emails/${idMail}`, {
                method: "PUT",
                body: JSON.stringify({
                  archived: false
                })
              })

              document.querySelector('#emails-view').style.cssText = `
              display: flex;
              flex-direction: column;
              flex-wrap: wrap;
              align-items: center;
              `;
              document.querySelector('#compose-view').style.display = 'none';
              document.querySelector("#emailOpenView").style.display = "none";
              document.querySelector("#ArchivedMail").style.display = "none";

              // Show the mailbox name
              document.querySelector('#emails-view').innerHTML = `<h3>${"Inbox".charAt(0).toUpperCase() + "Inbox".slice(1)}</h3>`;

              load_mailbox("inbox");

            })
          })

          .then(reply => {
            let subjectAntiguo = document.querySelector("#emailOpenView").querySelector("#subject").querySelector("strong").textContent;
            let bodyP = document.querySelector("#emailOpenView").querySelector("#body").textContent;
            let timestamp = document.querySelector("#emailOpenView").querySelector("#timestamp").textContent;
            let sender = document.querySelector("#emailOpenView").querySelector("#sender").querySelector("strong").textContent;
            let recipients = document.querySelector("#emailOpenView").querySelector("#recipients").querySelector("strong").textContent;
            let mailID = document.querySelector("#emailOpenView").querySelector("#id").textContent;

            document.querySelector("#reply").addEventListener("click", () =>  {
              console.log("Archive --- CLICK  --> reply");

              fetch(`/emails/${idMail}`, {
                method: "PUT",
                body: JSON.stringify({
                  read: true
                })
              });
              replyMail();
            });
          })
          .catch(error => console.log(error));
        });
      });
    })
    .catch(error => console.log(error));
  }
}
