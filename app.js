const url = "http://127.0.0.1:8000"

async function add_task() {

    let inp = document.getElementById("taskInput")

    let task = {

        task : inp.value,
        done : false

    }
    
    await fetch(url+"/tasks",{

        method : "POST",
        headers :{
           "Content-Type": "application/json"
        },

        body: JSON.stringify(task)
    })

    inp.value = ""
    loadTask()

}

async function loadTask() {

    let res = await fetch(url + "/tasks")
    let data = await res.json()

    let  list = document.getElementById("list")
    list.innerhtml = ""

    data.forEach(t => {

        let li = document.createElement("li")
        li.textContent = t.task + (t.done ? "\t\t"+"\u2714" : "")
        list.appendChild(li)

    })

}

loadTask()
