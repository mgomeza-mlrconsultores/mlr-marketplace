# Despliegue para toda la organizacion, sin que nadie ejecute comandos

Este es el procedimiento que hace que cualquier persona de MLR Consultores tenga el estandar disponible por el solo hecho de pertenecer a la organizacion.

Lo realiza **una vez** el propietario o administrador de la organizacion. Los demas no hacen nada.

## Requisito

Plan Team o Enterprise, con Cowork y Skills habilitados.

## Procedimiento

Entrar a la configuracion de administracion de la organizacion en claude.ai, apartado de **Plugins** dentro de Organization settings.

Hay dos vias, y para MLR conviene la segunda.

### Via A — subir el paquete

Pulsar **Add**, subir el archivo del plugin empaquetado y elegir el nivel de acceso.

Sirve cuando no se quiere depender de un repositorio. El limite es 50 MB por paquete.

### Via B — sincronizacion con el repositorio (recomendada)

Elegir **GitHub Sync** y conectar el repositorio `mgomeza-mlrconsultores/mlr-marketplace`. La autenticacion la resuelve la plataforma con la autorizacion del administrador, asi que **ninguna persona del equipo necesita credenciales de git ni acceso al repositorio**.

Esta es la via correcta para MLR por dos razones. El repositorio es privado y seguira siendolo. Y cada version nueva que se publique llega sola a todo el equipo, sin redistribuir nada.

## Nivel de acceso por plugin

Al dar de alta cada plugin, el administrador elige como se comporta:

| Nivel | Efecto |
|---|---|
| **Instalado por defecto** | Aparece ya activo para todos. Nadie ejecuta nada. **Es el nivel a elegir para los tres plugins de MLR.** |
| Requerido | Igual que el anterior, pero nadie puede desinstalarlo |
| Disponible | Aparece en el catalogo, cada persona decide |
| Oculto | No se ofrece |

Con **Instalado por defecto**, quien abra Claude siendo parte de la organizacion ya tiene el estandar cargado. Es exactamente el comportamiento que MLR busca: son las directivas generales de la firma, no una herramienta opcional.

## Que hace falta configurar en cada plugin

`mlr-orquestador`, `mlr-odoo` y `mlr-design`: instalado por defecto.

## Memoria en la nube

El plugin declara el servidor de memoria. Cada persona lo autoriza una vez en el navegador la primera vez que aparece. Ese paso no se puede centralizar porque la autorizacion es personal, y es el unico gesto que se pide al equipo.

## Alta de personas nuevas

Nada que hacer. Al sumarse a la organizacion, reciben los plugins ya instalados.

## Publicar una version nueva del estandar

Subir el cambio al repositorio y subir la version en `marketplace.json` y en el `plugin.json` correspondiente. La sincronizacion lo propaga. Nadie reinstala.

## Alternativa para Claude Code de escritorio

Si alguien del equipo usa Claude Code por linea de comandos, existe un archivo de politica gestionada que preinstala el marketplace y los plugins:

Windows: `C:\Program Files\ClaudeCode\managed-settings.json`
macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
Linux: `/etc/claude-code/managed-settings.json`

```json
{
  "extraKnownMarketplaces": {
    "mlr": {
      "source": { "source": "github", "repo": "mgomeza-mlrconsultores/mlr-marketplace" }
    }
  },
  "enabledPlugins": {
    "mlr-orquestador@mlr": true,
    "mlr-odoo@mlr": true,
    "mlr-design@mlr": true
  }
}
```

La politica gestionada gana sobre la configuracion del usuario y este no puede desactivarla.

**Advertencia.** Por esta via, al ser el repositorio privado, cada maquina necesita credenciales de git con acceso al repositorio. Es la razon por la que la sincronizacion desde el panel de administracion es preferible: ahi la autenticacion la resuelve la plataforma una sola vez.
