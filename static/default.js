let form_addTask = { 'state': 0 }
let form_removeTask = { 'state': 0 }
let form_addAssignee = { 'state': 0 }
let form_addSubTask = { 'state': 0 }
let errorMessage = { 'state': 0 }
let form_editSubTask = []
for (let i = 0; i < document.getElementsByClassName("fa-edit").length; i++) {
    form_editSubTask[i] = 0
}

addTask()
removeTask()
addAssignee()
addSubTask()
editSubTask()
taskAlreadyExists()
subTaskValidator()
removeSubTask()

function subTaskValidator() {
    let subTask_validator = document.getElementsByClassName("subTask_validator")
    for (let j = 0; j < subTask_validator.length; j++) {
        if (subTask_validator[j].dataset.subtaskState == 0) {
            subTask_validator[j].checked = true
            subTask_validator[j].nextElementSibling.classList.add('-line')
        }
        subTask_validator[j].addEventListener('click', (e) => {
            if (e.target.checked) {
                e.target.nextElementSibling.classList.add('-line')
                document.getElementsByClassName("subTask_state")[j].value = 0
                document.getElementsByClassName("subTaskList__subTask")[j].submit()
            } else {
                e.target.nextElementSibling.classList.remove('-line')
                document.getElementsByClassName("subTask_state")[j].value = 1
                document.getElementsByClassName("subTaskList__subTask")[j].submit()
            }
        })
    }
}

function addTask() { 
    document.getElementById('button_addTask').addEventListener('click', () => {
        hideAll('form_addTask')
        if (form_addTask.state == 0) show('form_addTask', form_addTask)
        else hide('form_addTask', form_addTask)        
    })
}

function removeTask() {
    let form = document.getElementById("form_removeTask")
    let button = document.getElementById("button_removeTask")
    if (button) {
        button.addEventListener('click', () => {
            hideAll('removeTask_confirm')
            if (form.dataset.idTask == 0 && form_removeTask.state == 0) show('noTask_alert', form_removeTask)
            else if (form.dataset.idTask != 0 && form_removeTask.state == 0) show('removeTask_confirm', form_removeTask)
            else { hide('removeTask_confirm', form_removeTask); hide('noTask_alert', form_removeTask) }
        })
    }
}

function addAssignee() { 
    let button = document.getElementById("button_addAssignee")
    if (button) {
        document.getElementById('button_addAssignee').addEventListener('click', () => {
            hideAll('form_addAssignee')
            if (form_addAssignee.state == 0) show('form_addAssignee', form_addAssignee)
            else hide('form_addAssignee', form_addAssignee)        
        })
    }
}

function addSubTask() {
    let button = document.getElementById("button_addSubTask")
    if (button) {
        button.addEventListener('click', () => {
            hideAll('form_addSubTask')
            if (form_addSubTask.state == 0) show('form_addSubTask', form_addSubTask) 
            else hide('form_addSubTask', form_addSubTask) 
        })
    }    
}

(function onDropDownHideOthers() {
    let button = document.getElementById("dropDown__task_button")
    button.addEventListener('click', (e) => {
        if (e.target.checked || !e.target.checked) {
            hideAll('x')
            for (let j = 0; j < document.getElementsByClassName("fa-edit").length; j++) {
                document.getElementsByClassName("subTask_title")[j].classList.remove("-hide")
            }
        }       
    })
})()

function editSubTask() {
    let button = document.getElementsByClassName("fa-edit")
    if (button) {        
        for (let i = 0; i < button.length; i++) {
            button[i].addEventListener('click', () => {
                let but = document.getElementById("dropDown__task_button")
                if (but.checked) but.checked = false
                hideAll('form_editSubTask')
                if (form_editSubTask[i] == 0 ) {
                    for (let j = 0; j < button.length; j++) {
                        hide("form_editSubTask", form_editSubTask, j)
                        document.getElementsByClassName("subTask_title")[j].classList.remove("-hide")
                    }
                    document.getElementsByClassName("subTask_title")[i].classList.add("-hide")
                    show("form_editSubTask", form_editSubTask, i)
                }
                else {
                    hide("form_editSubTask", form_editSubTask, i)
                    document.getElementsByClassName("subTask_title")[i].classList.remove("-hide")
                }
            })
        }        
    }    
}

function removeSubTask() {
    let button = document.getElementsByClassName("fa-trash-alt")
    if (button) {        
        for (let i = 0; i < button.length; i++) {
            button[i].addEventListener('click', () => {
                document.getElementsByClassName("button_removeSubTask")[i].click()
            })
        }
    }
}

function taskAlreadyExists() {
    if (document.getElementById('errorMessage_content').textContent != '') {
        if (errorMessage.state == 0) show('errorMessage', errorMessage) 
    }
    document.getElementById('errorMessage_ok').addEventListener('click', () => {
        if (errorMessage.state == 1) hide('errorMessage', errorMessage) 
    })
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

function hideAll(exception) {
    if (exception != 'form_addTask') {
        if (form_addTask.state == 1) hide('form_addTask', form_addTask)
    }
    if (exception != 'removeTask_confirm') {
        if (form_removeTask.state == 1) { hide('removeTask_confirm', form_removeTask); hide('noTask_alert', form_removeTask) }
    }
    if (exception != 'form_addAssignee') {
        if (form_addAssignee.state == 1) hide ('form_addAssignee', form_addAssignee)
    }
    if (exception != 'form_addSubTask') {
        if (form_addSubTask.state == 1 ) hide("form_addSubTask", form_addSubTask)
    }
    if (exception != 'form_editSubTask') {
        for (let i = 0; i < document.getElementsByClassName("fa-edit").length; i++) {           
            if (form_editSubTask[i] == 1 ) hide("form_editSubTask", form_editSubTask, i)
        }
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