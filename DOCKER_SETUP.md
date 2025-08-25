# DOCKER_SETUP.md

## Cómo levantar el proyecto con Docker

Sigue estos pasos para construir y ejecutar el contenedor Docker de este proyecto en Linux:

### 1. Requisitos previos
- Tener Docker instalado y en ejecución.

### 2. Construir la imagen Docker
Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
docker build -t contador-visitas .
```
Esto creará una imagen llamada `contador-visitas`.

### 3. Levantar el contenedor
Ejecuta el siguiente comando:

```bash
docker run -d -p 5000:5000 --name visitas contador-visitas
```
- `-d`: Ejecuta el contenedor en segundo plano.
- `-p 5000:5000`: Mapea el puerto 5000 del contenedor al 5000 de tu máquina.
- `--name visitas`: Asigna el nombre `visitas` al contenedor.

### 4. Acceder a la aplicación
Abre tu navegador y visita:
```
http://localhost:5000
```

---

## 1. ¿Qué pasa si corremos la imagen de Docker sin asignar ninguna flag a `docker run`? ¿Podemos usar la misma terminal para correr otros comandos?

Si ejecutas el contenedor con:

```zsh
docker run contador:latest
```

El contenedor se ejecuta en primer plano (modo interactivo). La terminal queda ocupada por el proceso del contenedor y no puedes usarla para otros comandos hasta que el contenedor termine o lo detengas con `Ctrl+C`.

---

## 2. El proyecto usa el puerto 5000. Intentar hacer `docker run` con y sin el parámetro correspondiente. ¿Qué ocurre en cada caso?

- **Sin el parámetro `-p 5000:5000`:**

  ```zsh
  docker run contador:latest
  ```

  El contenedor inicia, pero el puerto 5000 solo está disponible dentro del contenedor. No puedes acceder a la aplicación desde tu navegador en `localhost:5000`.

- **Con el parámetro `-p 5000:5000`:**

  ```zsh
  docker run -p 5000:5000 contador:latest
  ```

  El puerto 5000 del contenedor se publica en el puerto 5000 de tu máquina. Ahora puedes acceder a la aplicación en `http://localhost:5000`.

---

## 3. Ejecutar `docker stop <container>`. ¿Qué pasa si al hacer `docker run` no le asigno un nombre al contenedor? ¿Qué debo poner en `<container>` para poder hacer `docker stop <container>`?

Si no asignas un nombre al contenedor con `--name`, Docker le asigna un nombre aleatorio. Para detenerlo, necesitas el **ID** o el **nombre** del contenedor. Puedes obtenerlo con:

```zsh
docker ps
```

Luego ejecuta:

```zsh
docker stop <container_id_o_nombre>
```

Si quieres asignar un nombre al crear el contenedor:

```zsh
docker run --name mi_contenedor -p 5000:5000 contador:latest
```

---

## 4. Si corro el contenedor en segundo plano, no veo información de la dirección IP que necesito para usar mi proyecto. Documentar qué se debe poner en el navegador

Al ejecutar el contenedor en segundo plano (modo detached):

```zsh
docker run -d -p 5000:5000 contador:latest
```

La aplicación será accesible desde tu navegador en:

```
http://localhost:5000
```

No necesitas la IP del contenedor, solo accede a `localhost` en el puerto publicado.
