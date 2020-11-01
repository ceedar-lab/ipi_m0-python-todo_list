let form_addTask = { 'state': 0 }
let form_removeTask = { 'state': 0 }

addTask()
removeTask()

function addTask() {  
    let addTaskMenu_state = 0
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
        if (form.dataset.idTask == "0" && form_removeTask.state == 0) show('noTask_alert', form_removeTask)
        else if (form.dataset.idTask != "0" && form_removeTask.state == 0) show('removeTask_confirm', form_removeTask)
        else { hide('removeTask_confirm', form_removeTask); hide('noTask_alert', form_removeTask) }
    })
}

function show(id, stateId) {
    document.getElementById(id).classList.remove('-hide')
    stateId.state = 1
}

function hide(id, stateId) {
    document.getElementById(id).classList.add('-hide')
    stateId.state = 0
}

(function autoSubmit() {
    document.getElementById("taskList").addEventListener('change', () => {
        document.getElementById("form_taskList").submit()
    })
})()