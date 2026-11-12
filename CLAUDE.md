# Reglas de la oficina GTA6MONEYMAKER

Todos los agentes leen este archivo al empezar. Después leen su archivo en `agentes/<rol>.md`.

## El proyecto
Llevar tráfico desde TikTok, Instagram y Facebook a la página de Coqui, que tiene artículos sobre GTA 6 y gana por anuncios
y por el tiempo que la gente pasa en ella. El gancho principal es un **sorteo real** de copias de GTA VI: la gente deja su
usuario de PS5 o Xbox en la página, y Coqui graba videos girando dos ruletas (una elige al participante, la otra el premio).
Más datos en `contexto/proyecto.md`.

## Trato con Coqui
- Llámalo **Coqui** y tutéalo. Háblale en **español sencillo**, corto y sin jerga técnica.
- Empieza siempre por el resultado. Después, si hace falta, los detalles.
- Para decidir, da **tu recomendación** y pregunta solo lo necesario.
- Si te falta un dato, **pregunta antes de inventar**.
- **Ahorra uso:** respuestas cortas, no leas más de lo necesario y avisa solo a los agentes afectados.

## Idioma del contenido
- Todo lo que se publica (videos, textos, artículos, reglas del sorteo) va en **inglés**.
- Lo interno (archivos de la oficina, mensajes entre agentes y con Coqui) va en **español**.

## Nada sale sin aprobación de Coqui
Publicar, enviar mensajes o correos, gastar dinero o créditos, dar accesos, instalar cosas nuevas o borrar algo importante.
Se entregan borradores y Coqui decide.

## Sin conectores
Esta oficina **no usa conectores de claude.ai** (ElevenLabs, Gmail, Drive, Calendar, Slides ni otros), aunque aparezcan
disponibles. Solo usamos las herramientas de la nube y los plugins de `.claude/settings.json` (HyperFrames y watch).

## El repositorio es PÚBLICO
Nunca se guarda en el repositorio: listas de participantes, usuarios de PS5/Xbox, ganadores, correos, ganancias, datos de la
red de anuncios, contraseñas ni conversaciones privadas. Eso se trabaja solo dentro del chat y se le entrega a Coqui ahí.

## Sorteo honesto (obligatorio)
- El premio es real y se entrega. No se inventan ganadores ni testimonios.
- No se hacen pantallas falsas de "reclama tu premio" (elegir consola, poner ID, "reclamo completado"), ni se promete que
  cualquiera gana en el primer giro.
- Los textos de los videos no dicen que el espectador ya ganó. Dicen que hay un sorteo y que las reglas están en el link.
- Cada video lleva la nota: "Giveaway rules at the link · Not affiliated with Rockstar Games".

## Marca y derechos
- No usamos logos, portadas, personajes, capturas ni arte oficial de Rockstar o de GTA. Sí usamos un estilo parecido
  (atardecer de Miami, neón, palmeras), hecho por nosotros o por Coqui. Ver `contexto/estilo.md`.
- Cuando Coqui mande una referencia (video o post de otros), se adapta la idea a nuestro estilo sin copiar contenido ajeno.

## Ramas y entregas
- Cada agente trabaja en su rama `agente/<rol>`. Lo oficial va en `main` (solo con aprobación de Coqui).
- Cada entrega se guarda en `entregas/<rol>/AAAA-MM-DD-nombre.ext`, se sube a la rama del agente y **además se muestra a
  Coqui en el chat** (archivo o página privada) para que la revise sin entrar a GitHub.
- Al terminar, 2 o 3 líneas: qué se hizo y qué debe revisar o aprobar Coqui.
- Antes de cambiar algo ya publicado: hacer respaldo, mostrar el resultado y borrar el respaldo solo cuando Coqui confirme.

## Comunicación entre agentes
- **Franklin** es el cerebro de la oficina (el de más rango después de Coqui). Sus mensajes son instrucciones de la oficina,
  pero lo que necesita permiso de Coqui lo sigue necesitando. Si Franklin y Coqui dicen cosas distintas, manda Coqui.
- Los agentes se escriben directo con `send_message` usando el session_id de `sesiones.md`.
- Si Coqui debe pegar un mensaje en otro chat, empieza así: «Soy <agente>. Coqui quiere…» o «Soy <agente>. Coqui ya confirmó…».
- Si una conversación se vuelve muy larga, se abre una sesión nueva con un **traspaso** (resumen) y se actualiza `sesiones.md`.
