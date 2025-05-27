// ===== FUNCIONES DE UTILIDAD =====

/**
 * Valida que un campo no contenga solo números
 * @param {string} value - Valor a validar
 * @returns {boolean} - true si es válido, false si no
 */
function validateNotOnlyNumbers(value) {
  // Verifica si el valor contiene al menos un caracter que no sea número
  return !/^\d+$/.test(value)
}

/**
 * Valida un correo electrónico
 * @param {string} email - Correo a validar
 * @returns {boolean} - true si es válido, false si no
 */
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Valida que un número de celular tenga exactamente 10 dígitos
 * @param {string} phone - Número a validar
 * @returns {boolean} - true si es válido, false si no
 */
function validatePhone(phone) {
  return /^\d{10}$/.test(phone)
}

/**
 * Valida el tamaño y formato de una imagen
 * @param {File} file - Archivo a validar
 * @returns {Promise<boolean>} - Promise que resuelve a true si es válido, false si no
 */
function validateImage(file) {
  return new Promise((resolve) => {
    // Verificar el tipo de archivo
    if (!file.type.startsWith("image/")) {
      alert("El archivo debe ser una imagen")
      resolve(false)
      return
    }

    // Verificar el tamaño (máximo 2MB)
    if (file.size > 2 * 1024 * 1024) {
      alert("La imagen no debe superar los 2MB")
      resolve(false)
      return
    }

    // Verificar dimensiones
    const img = new Image()
    img.onload = () => {
      URL.revokeObjectURL(img.src)
      if (img.width > 1000 || img.height > 1000) {
        alert("La imagen no debe superar los 1000x1000 píxeles")
        resolve(false)
      } else {
        resolve(true)
      }
    }
    img.onerror = () => {
      URL.revokeObjectURL(img.src)
      alert("No se pudo cargar la imagen")
      resolve(false)
    }
    img.src = URL.createObjectURL(file)
  })
}

/**
 * Muestra una previsualización de la imagen seleccionada
 * @param {File} file - Archivo de imagen
 * @param {string} previewId - ID del elemento donde mostrar la previsualización
 */
function showImagePreview(file, previewId) {
  const preview = document.getElementById(previewId)
  if (preview) {
    preview.src = URL.createObjectURL(file)
    preview.onload = () => {
      URL.revokeObjectURL(preview.src)
    }
  }
}

/**
 * Guarda los datos de una persona en localStorage
 * @param {Object} personData - Datos de la persona
 */
function savePersonData(personData) {
  // Obtener datos existentes o inicializar array vacío
  const existingData = JSON.parse(localStorage.getItem("personasData")) || []

  // Agregar nueva persona
  existingData.push({
    ...personData,
    id: Date.now(), // Usar timestamp como ID único
  })

  // Guardar en localStorage
  localStorage.setItem("personasData", JSON.stringify(existingData))

  // Registrar en el log
  saveLogEntry({
    fecha: new Date(),
    usuario: "Usuario Actual",
    accion: "crear",
    documento: personData.nroDocumento,
    detalles: `Creación de registro para ${personData.primerNombre} ${personData.apellidos}`,
  })
}

/**
 * Actualiza los datos de una persona en localStorage
 * @param {Object} personData - Datos actualizados de la persona
 */
function updatePersonData(personData) {
  // Obtener datos existentes
  const existingData = JSON.parse(localStorage.getItem("personasData")) || []

  // Buscar la persona por número de documento
  const index = existingData.findIndex(
    (p) => p.tipoDocumento === personData.tipoDocumento && p.nroDocumento === personData.nroDocumento,
  )

  if (index !== -1) {
    // Actualizar datos
    existingData[index] = {
      ...existingData[index],
      ...personData,
    }

    // Guardar en localStorage
    localStorage.setItem("personasData", JSON.stringify(existingData))

    // Registrar en el log
    saveLogEntry({
      fecha: new Date(),
      usuario: "Usuario Actual",
      accion: "modificar",
      documento: personData.nroDocumento,
      detalles: `Modificación de registro para ${personData.primerNombre} ${personData.apellidos}`,
    })

    return true
  }

  return false
}

/**
 * Elimina una persona de localStorage
 * @param {string} tipoDocumento - Tipo de documento
 * @param {string} nroDocumento - Número de documento
 * @returns {boolean} - true si se eliminó, false si no se encontró
 */
function deletePersonData(tipoDocumento, nroDocumento) {
  // Obtener datos existentes
  const existingData = JSON.parse(localStorage.getItem("personasData")) || []

  // Buscar la persona
  const index = existingData.findIndex((p) => p.tipoDocumento === tipoDocumento && p.nroDocumento === nroDocumento)

  if (index !== -1) {
    const personData = existingData[index]

    // Eliminar del array
    existingData.splice(index, 1)

    // Guardar en localStorage
    localStorage.setItem("personasData", JSON.stringify(existingData))

    // Registrar en el log
    saveLogEntry({
      fecha: new Date(),
      usuario: "Usuario Actual",
      accion: "eliminar",
      documento: nroDocumento,
      detalles: `Eliminación de registro para ${personData.primerNombre} ${personData.apellidos}`,
    })

    return true
  }

  return false
}

/**
 * Busca personas según criterios de filtro
 * @param {Object} filters - Criterios de búsqueda
 * @returns {Array} - Array de personas que coinciden con los filtros
 */
function searchPersonData(filters) {
  // Obtener datos existentes
  const existingData = JSON.parse(localStorage.getItem("personasData")) || []

  // Filtrar según criterios
  return existingData.filter((person) => {
    for (const key in filters) {
      if (filters[key] && person[key] !== filters[key]) {
        return false
      }
    }
    return true
  })
}

/**
 * Guarda una entrada en el log
 * @param {Object} logEntry - Datos de la entrada de log
 */
function saveLogEntry(logEntry) {
  // Obtener log existente o inicializar array vacío
  const existingLog = JSON.parse(localStorage.getItem("activityLog")) || []

  // Agregar nueva entrada
  existingLog.push(logEntry)

  // Guardar en localStorage
  localStorage.setItem("activityLog", JSON.stringify(existingLog))
}

/**
 * Busca entradas de log según criterios
 * @param {Object} filters - Criterios de búsqueda
 * @returns {Array} - Array de entradas que coinciden con los filtros
 */
function searchLogEntries(filters) {
  // Obtener log existente
  const existingLog = JSON.parse(localStorage.getItem("activityLog")) || []

  // Filtrar según criterios
  return existingLog.filter((entry) => {
    for (const key in filters) {
      if (filters[key]) {
        if (key === "fecha") {
          // Comparar solo la fecha (no la hora)
          const entryDate = new Date(entry.fecha).toLocaleDateString()
          const filterDate = new Date(filters.fecha).toLocaleDateString()
          if (entryDate !== filterDate) {
            return false
          }
        } else if (entry[key] !== filters[key]) {
          return false
        }
      }
    }
    return true
  })
}

/**
 * Simula una consulta en lenguaje natural
 * @param {string} query - Consulta en lenguaje natural
 * @returns {string} - Respuesta simulada
 */
function simulateLLMQuery(query) {
  // Esta es una simulación simple
  if (!query.trim()) {
    return "Por favor, ingrese una consulta."
  }

  // Registrar en el log
  saveLogEntry({
    fecha: new Date(),
    usuario: "Usuario Actual",
    accion: "consultar_llm",
    documento: "",
    detalles: `Consulta LLM: "${query}"`,
  })

  // Simular tiempo de respuesta
  return `Respuesta simulada para: "${query}"
    
Se encontraron 3 registros relacionados con su consulta.

1. Juan Pérez (CC: 1234567890)
   - Correo: juan.perez@ejemplo.com
   - Teléfono: +57 3001234567

2. María López (CC: 0987654321)
   - Correo: maria.lopez@ejemplo.com
   - Teléfono: +57 3109876543

3. Carlos Rodríguez (TI: 1122334455)
   - Correo: carlos.rodriguez@ejemplo.com
   - Teléfono: +57 3201122334

Esta es una respuesta simulada para demostración.`
}

// ===== INICIALIZACIÓN Y MANEJO DE EVENTOS =====

// Esperar a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", () => {
  // ===== FORMULARIO DE CREAR PERSONA =====
  const crearPersonaForm = document.getElementById("crear-persona-form")
  if (crearPersonaForm) {
    crearPersonaForm.addEventListener("submit", async (e) => {
      e.preventDefault()

      // Validar campos
      const primerNombre = document.getElementById("primer-nombre").value
      const apellidos = document.getElementById("apellidos").value
      const correo = document.getElementById("correo").value
      const celular = document.getElementById("celular").value
      const fotoInput = document.getElementById("foto")

      if (!validateNotOnlyNumbers(primerNombre)) {
        alert("El primer nombre no puede contener solo números")
        return
      }

      if (!validateNotOnlyNumbers(apellidos)) {
        alert("Los apellidos no pueden contener solo números")
        return
      }

      if (!validateEmail(correo)) {
        alert("El correo electrónico no es válido")
        return
      }

      if (!validatePhone(celular)) {
        alert("El celular debe tener exactamente 10 dígitos numéricos")
        return
      }

      // Validar imagen si se ha seleccionado
      if (fotoInput.files.length > 0) {
        const isValid = await validateImage(fotoInput.files[0])
        if (!isValid) return
      }

      // Recopilar datos del formulario
      const personData = {
        tipoDocumento: document.getElementById("tipo-documento").value,
        nroDocumento: document.getElementById("nro-documento").value,
        primerNombre: primerNombre,
        segundoNombre: document.getElementById("segundo-nombre").value,
        apellidos: apellidos,
        fechaNacimiento: document.getElementById("fecha-nacimiento").value,
        genero: document.getElementById("genero").value,
        correo: correo,
        celular: celular,
        fotoUrl: fotoInput.files.length > 0 ? "foto_simulada.jpg" : "placeholder.png",
      }

      // Guardar datos
      savePersonData(personData)

      alert("Persona creada exitosamente")
      crearPersonaForm.reset()
      document.getElementById("photo-preview").src = "assets/img/placeholder.png"
    })

    // Manejar previsualización de imagen
    const fotoInput = document.getElementById("foto")
    if (fotoInput) {
      fotoInput.addEventListener("change", function () {
        if (this.files.length > 0) {
          showImagePreview(this.files[0], "photo-preview")
        }
      })
    }
  }

  // ===== FORMULARIO DE MODIFICAR DATOS =====
  const modificarDatosForm = document.getElementById("modificar-datos-form")
  if (modificarDatosForm) {
    // Buscar persona por ID
    const buscarPersonaInput = document.getElementById("buscar-persona")
    if (buscarPersonaInput) {
      buscarPersonaInput.addEventListener("keyup", function (e) {
        if (e.key === "Enter") {
          const nroDocumento = this.value.trim()
          if (nroDocumento) {
            // Simulación de búsqueda
            const existingData = JSON.parse(localStorage.getItem("personasData")) || []
            const person = existingData.find((p) => p.nroDocumento === nroDocumento)

            if (person) {
              // Llenar formulario con datos
              document.getElementById("tipo-documento").value = person.tipoDocumento
              document.getElementById("nro-documento").value = person.nroDocumento
              document.getElementById("primer-nombre").value = person.primerNombre
              document.getElementById("segundo-nombre").value = person.segundoNombre || ""
              document.getElementById("apellidos").value = person.apellidos
              document.getElementById("fecha-nacimiento").value = person.fechaNacimiento
              document.getElementById("genero").value = person.genero
              document.getElementById("correo").value = person.correo
              document.getElementById("celular").value = person.celular

              // Mostrar foto
              document.getElementById("photo-preview").src =
                person.fotoUrl === "placeholder.png" ? "assets/img/placeholder.png" : person.fotoUrl
            } else {
              alert("No se encontró ninguna persona con ese número de documento")
            }
          }
        }
      })
    }

    // Manejar envío del formulario
    modificarDatosForm.addEventListener("submit", async (e) => {
      e.preventDefault()

      // Validaciones similares a crear persona
      const primerNombre = document.getElementById("primer-nombre").value
      const apellidos = document.getElementById("apellidos").value
      const correo = document.getElementById("correo").value
      const celular = document.getElementById("celular").value
      const fotoInput = document.getElementById("foto")

      if (!validateNotOnlyNumbers(primerNombre)) {
        alert("El primer nombre no puede contener solo números")
        return
      }

      if (!validateNotOnlyNumbers(apellidos)) {
        alert("Los apellidos no pueden contener solo números")
        return
      }

      if (!validateEmail(correo)) {
        alert("El correo electrónico no es válido")
        return
      }

      if (!validatePhone(celular)) {
        alert("El celular debe tener exactamente 10 dígitos numéricos")
        return
      }

      // Validar imagen si se ha seleccionado
      if (fotoInput.files.length > 0) {
        const isValid = await validateImage(fotoInput.files[0])
        if (!isValid) return
      }

      // Recopilar datos del formulario
      const personData = {
        tipoDocumento: document.getElementById("tipo-documento").value,
        nroDocumento: document.getElementById("nro-documento").value,
        primerNombre: primerNombre,
        segundoNombre: document.getElementById("segundo-nombre").value,
        apellidos: apellidos,
        fechaNacimiento: document.getElementById("fecha-nacimiento").value,
        genero: document.getElementById("genero").value,
        correo: correo,
        celular: celular,
        fotoUrl: fotoInput.files.length > 0 ? "foto_actualizada.jpg" : document.getElementById("photo-preview").src,
      }

      // Actualizar datos
      const updated = updatePersonData(personData)

      if (updated) {
        alert("Datos actualizados exitosamente")
        document.getElementById("buscar-persona").value = ""
        modificarDatosForm.reset()
        document.getElementById("photo-preview").src = "assets/img/placeholder.png"
      } else {
        alert("No se pudo actualizar. Verifique que la persona exista.")
      }
    })

    // Manejar previsualización de imagen
    const fotoInput = document.getElementById("foto")
    if (fotoInput) {
      fotoInput.addEventListener("change", function () {
        if (this.files.length > 0) {
          showImagePreview(this.files[0], "photo-preview")
        }
      })
    }
  }

  // ===== FORMULARIO DE ELIMINAR PERSONA =====
  const eliminarPersonaForm = document.getElementById("eliminar-persona-form")
  if (eliminarPersonaForm) {
    // Buscar persona por ID
    const buscarPersonaInput = document.getElementById("buscar-persona")
    if (buscarPersonaInput) {
      buscarPersonaInput.addEventListener("keyup", function (e) {
        if (e.key === "Enter") {
          const nroDocumento = this.value.trim()
          if (nroDocumento) {
            // Simulación de búsqueda
            const existingData = JSON.parse(localStorage.getItem("personasData")) || []
            const person = existingData.find((p) => p.nroDocumento === nroDocumento)

            if (person) {
              // Llenar formulario con datos (solo lectura)
              document.getElementById("tipo-documento").value = person.tipoDocumento
              document.getElementById("nro-documento").value = person.nroDocumento
              document.getElementById("primer-nombre").value = person.primerNombre
              document.getElementById("segundo-nombre").value = person.segundoNombre || ""
              document.getElementById("apellidos").value = person.apellidos
              document.getElementById("fecha-nacimiento").value = person.fechaNacimiento
              document.getElementById("genero").value = person.genero
              document.getElementById("correo").value = person.correo
              document.getElementById("celular").value = person.celular

              // Mostrar foto
              document.getElementById("photo-preview").src =
                person.fotoUrl === "placeholder.png" ? "assets/img/placeholder.png" : person.fotoUrl
            } else {
              alert("No se encontró ninguna persona con ese número de documento")
            }
          }
        }
      })
    }

    // Manejar envío del formulario
    eliminarPersonaForm.addEventListener("submit", (e) => {
      e.preventDefault()

      const tipoDocumento = document.getElementById("tipo-documento").value
      const nroDocumento = document.getElementById("nro-documento").value

      if (!tipoDocumento || !nroDocumento) {
        alert("Debe buscar una persona primero")
        return
      }

      // Confirmar eliminación
      if (confirm("¿Está seguro de que desea eliminar esta persona?")) {
        // Eliminar datos
        const deleted = deletePersonData(tipoDocumento, nroDocumento)

        if (deleted) {
          alert("Persona eliminada exitosamente")
          document.getElementById("buscar-persona").value = ""
          eliminarPersonaForm.reset()
          document.getElementById("photo-preview").src = "assets/img/placeholder.png"
        } else {
          alert("No se pudo eliminar. Verifique que la persona exista.")
        }
      }
    })
  }

  // ===== FORMULARIO DE CONSULTA =====
  const consultaForm = document.getElementById("consulta-form")
  if (consultaForm) {
    consultaForm.addEventListener("submit", (e) => {
      e.preventDefault()

      // Recopilar filtros
      const filters = {
        tipoDocumento: document.getElementById("tipo-documento").value,
        nroDocumento: document.getElementById("nro-documento").value,
        primerNombre: document.getElementById("primer-nombre").value,
        segundoNombre: document.getElementById("segundo-nombre").value,
        apellidos: document.getElementById("apellidos").value,
        genero: document.getElementById("genero").value,
        fechaNacimiento: document.getElementById("fecha-nacimiento").value,
        correo: document.getElementById("correo").value,
        celular: document.getElementById("celular").value,
      }

      // Buscar personas que coincidan
      const results = searchPersonData(filters)

      // Mostrar resultados en la tabla
      const tbody = document.querySelector("#resultados-tabla tbody")
      tbody.innerHTML = ""

      if (results.length === 0) {
        const row = document.createElement("tr")
        row.innerHTML = '<td colspan="6">No se encontraron resultados</td>'
        tbody.appendChild(row)
      } else {
        results.forEach((person) => {
          const row = document.createElement("tr")
          row.innerHTML = `
                        <td>${person.tipoDocumento}</td>
                        <td>${person.nroDocumento}</td>
                        <td>${person.primerNombre} ${person.segundoNombre || ""}</td>
                        <td>${person.apellidos}</td>
                        <td>${person.genero}</td>
                        <td>${person.correo}</td>
                    `
          tbody.appendChild(row)
        })
      }

      // Registrar en el log
      saveLogEntry({
        fecha: new Date(),
        usuario: "Usuario Actual",
        accion: "consultar",
        documento: filters.nroDocumento || "múltiple",
        detalles: `Consulta de datos: ${results.length} resultados`,
      })
    })
  }

  // ===== CONSULTA LLM =====
  const btnConsultarLLM = document.getElementById("btn-consultar-llm")
  if (btnConsultarLLM) {
    btnConsultarLLM.addEventListener("click", () => {
      const query = document.getElementById("consulta-llm").value
      const responseElement = document.getElementById("llm-response")

      // Mostrar indicador de carga
      responseElement.textContent = "Procesando consulta..."

      // Simular tiempo de respuesta
      setTimeout(() => {
        const response = simulateLLMQuery(query)
        responseElement.textContent = response
      }, 1500)
    })
  }

  // ===== CONSULTA LOG =====
  const logForm = document.getElementById("log-form")
  if (logForm) {
    logForm.addEventListener("submit", (e) => {
      e.preventDefault()

      // Recopilar filtros
      const filters = {
        tipoTransaccion: document.getElementById("tipo-transaccion").value,
        documento: document.getElementById("nro-documento").value,
        fecha: document.getElementById("fecha").value,
      }

      // Buscar entradas de log
      const results = searchLogEntries(filters)

      // Mostrar resultados en la tabla
      const tbody = document.querySelector("#log-tabla tbody")
      tbody.innerHTML = ""

      if (results.length === 0) {
        const row = document.createElement("tr")
        row.innerHTML = '<td colspan="6">No se encontraron registros en el log</td>'
        tbody.appendChild(row)
      } else {
        results.forEach((entry) => {
          const date = new Date(entry.fecha)
          const row = document.createElement("tr")
          row.innerHTML = `
                        <td>${date.toLocaleDateString()}</td>
                        <td>${date.toLocaleTimeString()}</td>
                        <td>${entry.usuario}</td>
                        <td>${entry.accion}</td>
                        <td>${entry.documento || "-"}</td>
                        <td>${entry.detalles}</td>
                    `
          tbody.appendChild(row)
        })
      }
    })
  }

  // ===== BOTÓN DESACTIVAR CONSULTA =====
  const btnDesactivarConsulta = document.getElementById("desactivar-consulta")
  if (btnDesactivarConsulta) {
    btnDesactivarConsulta.addEventListener("click", () => {
      alert("Funcionalidad de consulta desactivada")
    })
  }
})
