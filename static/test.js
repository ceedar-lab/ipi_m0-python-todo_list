let form_addTask = { 'state': 0 }
let form_removeTask = { 'state': 0 }
let form_addSubTask = { 'state': 0 }
let form_editSubTask = []
for (let i = 0; i < document.getElementsByClassName("button_editSubTask").length; i++) {
    form_editSubTask[i] = 0
}

addTask()
removeTask()
addSubTask()
editSubTask()

function addTask() { 
    document.getElementById('button_addTask').addEventListener('click', () => {
        if (form_removeTask.state == 1) { hide('removeTask_confirm', form_removeTask); hide('noTask_alert', form_removeTask) }
        if (form_addTask.state == 0) show('form_addTask', form_addTask)
        else hide('form_addTask', form_addTask)        
    })
}

function removeTask() {
    let form = document.getElementById("form_removeTask")
    document.getElementById("button_removeTask").addEventListener('click', () => {
        if (form_addTask.state == 1) hide('form_addTask', form_addTask)
        if (form.dataset.idTask == 0 && form_removeTask.state == 0) show('noTask_alert', form_removeTask)
        else if (form.dataset.idTask != 0 && form_removeTask.state == 0) show('removeTask_confirm', form_removeTask)
        else { hide('removeTask_confirm', form_removeTask); hide('noTask_alert', form_removeTask) }
    })
}

function addSubTask() {
    let button = document.getElementById("button_addSubTask")
    if (button) {
        button.addEventListener('click', () => {
            if (form_addSubTask.state == 0) show('form_addSubTask', form_addSubTask) 
            else hide('form_addSubTask', form_addSubTask) 
        })
    }    
}

function editSubTask() {
    let button = document.getElementsByClassName("button_editSubTask")
    if (button) {        
        for (let i = 0; i < button.length; i++) {
            button[i].addEventListener('click', () => {            
                if (form_editSubTask[i] == 0 ) show("form_editSubTask", form_editSubTask, i)
                else hide("form_editSubTask", form_editSubTask, i)
            })
        }        
    }    
}

function show(id, form, i) {
    if ('state' in form) {
        document.getElementById(id).classList.remove('-hide')
        form.state = 1
    } else {
        document.querySelectorAll("."+id)[i].classList.remove('-hide')
        form[i] = 1
    }    
}

function hide(id, form, i) {
    if ('state' in form) {
        document.getElementById(id).classList.add('-hide')
        form.state = 0
    } else {
        document.querySelectorAll("."+id)[i].classList.add('-hide')
        form[i] = 0
    }
}

(function autoSubmit() {
    document.getElementById("taskList").addEventListener('change', () => {
        document.getElementById("form_taskList").submit()
    })
})()