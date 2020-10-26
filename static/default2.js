function do_ajax() {
    var req = new XMLHttpRequest();
    var result = document.getElementById('result');
    req.onreadystatechange = function()
    {
      if(this.readyState == 4 && this.status == 200) {
        result.innerHTML = this.responseText;
      } else {
        result.innerHTML = "処理中...";
      }
    }

    req.open('POST', '/', true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send("name=" + document.getElementById('name').value);
}

function req_show_color() {    
  let xhr = new XMLHttpRequest
  xhr.open('POST', '/', true)
  xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
  xhr.send("name=" + document.getElementById('name2').value)
  xhr.onload = () => {
      if (xhr.readyState == 4 && xhr.status == 200) show_color(xhr.responseText)
      else show_color('pas de réponse')
  }
}

function show_color(res) {
  let form = document.getElementById("form2")
  let html = `<div>
                <p>${res}</p>
              </div>`
  form.insertAdjacentHTML('afterend', html)
}

document.getElementById("btn-post2").addEventListener('click', req_show_color)