// Mini validación y demo de manejo de envío
const form = document.getElementById('loginForm');
const gbtn = document.getElementById('googleBtn');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const data = new FormData(form);
  const email = data.get('email')?.trim();
  const pass = data.get('password')?.trim();
  let ok = true;

  const emailErr = document.querySelector('[data-for="email"]');
  const passErr = document.querySelector('[data-for="password"]');
  emailErr.textContent = '';
  passErr.textContent = '';

  if(!email || !/.+@.+\..+/.test(email)){
    emailErr.textContent = 'Ingresá un correo válido.';
    ok = false;
  }
  if(!pass || pass.length < 6){
    passErr.textContent = 'La contraseña debe tener al menos 6 caracteres.';
    ok = false;
  }

  if(ok){
    // Aquí conectarías tu backend / auth provider
    alert('Login OK! (demo)\nEmail: ' + email);
  }
});

gbtn.addEventListener('click', () => {
  alert('Continuar con Google (demo)');
});
