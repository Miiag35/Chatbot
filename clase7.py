#python -m streamlit run clase7.py -> para que aparezca la pág en el navegador
#streamlit run clase7.py

#secrets.toml

import streamlit as st
from groq import Groq

clave_usuario = ""
usuario = ""
modelo_actual = ""
mensaje = ""
#modelos = ["Modelos1", "Modelos2", "Modelos3"]
modelos = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]

# Creamos el usuario
def crear_usuario_groq():
    clave_usuario = st.secrets["CLAVE_API"]
    return Groq(api_key = clave_usuario)

# Configurar modelo
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    #retornamos la funcion que procesa el msj del usuario
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream = True
)
    
#
def generar_respuesta(chat_completo):
      respuesta_completa = ""
      for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
      return respuesta_completa
    
# Acá guardamos el mensaje dentro de la lista "mensajes"
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

# 
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]): #chat_message: mostrar cosas en pantalla
            st.markdown(mensaje["content"])
            
#
def area_de_chat():
    contenedor_del_chat = st.container(height=600, border=True)
    with contenedor_del_chat:
        mostrar_historial()

# Creamos un estado donde el usuario va a poder guardar sus msjs 
def inicializar_estado():
    if "mensajes" not in st.session_state:
        # Creamos la lista de mensajes
        st.session_state.mensajes = [] 

# Función para instanciar la página
def configurar_pagina():
    # Cambiar nombre de pestaña
    st.set_page_config("Mi chat AI")
    # Agregamos un titulo
    st.title("Mi súper chat bot")
    # Agregamos un sidebar
    st.sidebar.title("Sidebar de modelos")
    m = st.sidebar.selectbox("Modelos", modelos, index=0)
    return m

# Bloque de ejecución
def main():
    # Llamamos al estado de mensaje
    inicializar_estado()

    # Creamos un usuasio a partir de la CLAVE_API
    usuario = crear_usuario_groq()

    # Configuramos la página y seleccionamos un modelo
    modelo_actual = configurar_pagina()

    # Llamamos al area del chat
    area_de_chat()

    # Creamos el chat box
    mensaje = st.chat_input("Escribí tu mensaje:")

    # Procesar una respuesta a partir de un modelo elegido
    respuesta_chat_bot = ""
    
    if mensaje:
        actualizar_historial("user", mensaje, "🦖")
        respuesta_chat_bot = configurar_modelo(usuario, modelo_actual, mensaje)
        #actualizar_historial("assistant", respuesta_chat_bot, "👻")
        #st.rerun()
        
    if respuesta_chat_bot:
        with st.chat_message("assistant"):
            respuesta_completa = st.write_stream(generar_respuesta(respuesta_chat_bot))
            actualizar_historial("assistant", respuesta_completa, "👻")
            
            st.rerun()

if __name__ == "__main__":
    main()


