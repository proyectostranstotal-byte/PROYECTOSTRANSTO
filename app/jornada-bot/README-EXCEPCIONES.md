# Excepciones a la racha de días corridos (jornada-bot)

Permite marcar a mano que un chofer descansó aunque el descanso no haya llegado a las 36 h
que el bot exige para cortar la racha.

## Instalar (una sola vez, en la PC NDIFABIO)

1. Copiar `excepciones-racha.js` y `excepciones-racha.json` a `C:\jornada-bot\`.
2. En `C:\jornada-bot\rachas.js`, en el punto donde queda definido el número de días corridos
   de cada chofer (lo que se muestra como "Días acumulados" y decide si la jornada se reduce a
   10 h), agregar:

   ```js
   const { aplicarExcepcion } = require('./excepciones-racha');
   // ...
   dias = aplicarExcepcion(nombreChofer, dias);
   ```

   Si `rachas.js` se usa tanto desde `index.js` (aviso de las 14:00) como desde
   `exceso-jornada.js` (reporte de las 08:00), con ese único cambio quedan cubiertos los dos.
   Si cada uno calcula los días por su cuenta, aplicar la misma línea en ambos.

3. Probar sin mandar nada:

   ```
   cd C:\jornada-bot
   node -e "console.log(require('./excepciones-racha').aplicarExcepcion('Broya Marcos', 12))"
   ```

   Hoy (24/10) tiene que imprimir `2`.

## Cargar una excepción

Agregar una entrada en `excepciones-racha.json`:

```json
{ "chofer": "Apellido Nombre", "inicioRacha": "YYYY-MM-DD", "motivo": "…", "vence": "YYYY-MM-DD" }
```

- `inicioRacha`: primer día de la racha nueva (el día que volvió a trabajar después del descanso).
- `vence` (opcional): fecha a partir de la cual la excepción se ignora.

La excepción nunca aumenta la cuenta: devuelve el menor valor entre lo que calculó el bot y
los días desde `inicioRacha`. Cuando el chofer haga un descanso real de 36 h, el bot vuelve a
contar desde 1 y la excepción deja de tener efecto sola.

## Caso cargado: Broya Marcos

Descansó 33 h 05 min (21/10 21:21 → 23/10 06:26). Se acepta como descanso por decisión de
NDiFabio: 23/10 = día 1, 24/10 = día 2. Vence el 15/11.
