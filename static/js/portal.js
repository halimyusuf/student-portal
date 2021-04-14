const portalForm = document.querySelector('.portal-form');
const inputEle = document.querySelectorAll('.portal-form input');
const stateSelect = document.querySelector('.state-select');
let localGovtSelect = document.querySelector('.local-govt-select');
let addressEle = document.querySelector('#inputAddress');

// populate states in select field
let opt;
for (let i = 0; i < states.length; i++) {
  opt = document.createElement('option');
  opt.setAttribute('value', i);
  opt.innerText = states[i].state;
  stateSelect.appendChild(opt);
}
// state select population ends here

// function to remove all element children, except a default child
function removeChildren(element, def) {
  let defEle = null;
  if (def !== undefined) {
    if (element.lastElementChild) {
      let tag = element.lastElementChild.tagName;
      defEle = document.createElement(tag);
      defEle.innerText = def;
    }
  }
  while (element.lastElementChild) {
    element.removeChild(element.lastElementChild);
  }
  if (defEle !== null) {
    element.appendChild(defEle);
  }
  return element;
}

// state select change event listener, populates local govt select options
stateSelect.addEventListener('change', () => {
  const ind = stateSelect.value;
  localGovtSelect = removeChildren(localGovtSelect, 'Select Local Government');
  local_govts = states[ind].local;
  let opt;
  for (let i = 0; i < local_govts.length; i++) {
    opt = document.createElement('option');
    opt.setAttribute('value', local_govts[i]);
    opt.innerText = local_govts[i];
    localGovtSelect.appendChild(opt);
  }
});

// handles portal form submission
portalForm.addEventListener('submit', () => {
  // create an instance of form data
  const formData = new FormData();
  formData.append('file', inputEle[0].files[0]);
  for (let input of inputEle) {
    if (input.type == 'radio') {
      if (input.checked) {
        formData.append(input.name, input.value);
      }
    } else {
      formData.append(input.name, input.value);
    }
  }
  formData.append('state_of_origin', states[stateSelect.value].state);
  formData.append('local_govt', localGovtSelect.value);
  formData.append('address', addressEle.value);
  axios
    .post('/students/new', formData)
    .then(() => {
      location.replace('/admin/dashboard');
    })
    .catch((err) => {
      console.log(err);
    });
});
