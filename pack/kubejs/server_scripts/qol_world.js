// World QoL (user request 2026-10-18): longer days and less rain in the Overworld.
// Long days come from the user's Wardaddy ATM10 server tweak (zz_custom/long_days.js).

// --- Longer days. DAY_MULT 2 = daytime lasts 2x as long (20 min instead of 10). Night is unchanged.
// Works by holding the clock back on (DAY_MULT - 1) of every DAY_MULT ticks while the sun is up.
const WB_DAY_MULT = 2
// --- Less rain. When the weather flips, vanilla has just rolled how long the new spell lasts (rainTime counts down to
// the next flip): dry spells (12000-180000 ticks) are stretched, rain (12000-24000 ticks) is cut short.
const WB_DRY_MULT = 2
const WB_RAIN_MULT = 0.5

const $WbGameRules = Java.loadClass('net.minecraft.world.level.GameRules')
let wbDayTick = 0
let wbWasRaining = null

ServerEvents.tick(event => {
  let level = event.server.overworld()
  let rules = level.getGameRules()

  if (WB_DAY_MULT > 1 && rules.getBoolean($WbGameRules.RULE_DAYLIGHT)) {
    let t = level.getDayTime()
    if (t % 24000 < 12000) { // day only; night runs at normal speed
      wbDayTick++
      if (wbDayTick % WB_DAY_MULT != 0) level.setDayTime(t - 1)
    }
  }

  if (event.server.getTickCount() % 20 != 0 || !rules.getBoolean($WbGameRules.RULE_WEATHER_CYCLE)) return
  let data = level.getLevelData()
  let raining = data.isRaining()
  if (wbWasRaining === null || raining == wbWasRaining) { wbWasRaining = raining; return }
  wbWasRaining = raining
  if (data.getClearWeatherTime() > 0) return // /weather clear is in charge
  let mult = raining ? WB_RAIN_MULT : WB_DRY_MULT
  data.setRainTime(Math.max(20, Math.floor(data.getRainTime() * mult)))
})
