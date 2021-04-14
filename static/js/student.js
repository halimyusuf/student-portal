const changeStatus = document.querySelector('#change-status');
const changeStatusBtn = document.querySelector('.change-status-btn');
const studentStatus = document.querySelector('.student-status div').textContent;

// toggles submit button hide
changeStatus.addEventListener('change', () => {
  if (changeStatus.value.toLowerCase() !== studentStatus.toLowerCase()) {
    changeStatusBtn.classList.remove('hide');
  } else {
    changeStatusBtn.classList.add('hide');
  }
});

// handles update of status
changeStatusBtn.addEventListener('click', () => {
  const id = changeStatusBtn.getAttribute('id').split('-')[1];
  axios
    .post(`/student/status/${id}`, { status: changeStatus.value })
    .then(() => {
      location.reload();
    })
    .catch((err) => {
      console.log(err);
    });
});
