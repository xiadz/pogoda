%include header

<section>
  <strong>Current&nbsp;readings</strong>
</section>

<section id="pageContent">
  <article>
    <table>
      <!-- Temperature -->
      % if temp is not None:
          <tr><td>Temperature:</td>
              <td>{{ temp }} °C</td></tr>
      % end

      <tr><td colspan=2></td></tr>

      <!-- Humidity -->
      % if hmdt is not None:
          <tr><td>Humidity:</td>
              <td>{{ hmdt }} %</td></tr>
      % end
      % if vapor_pres is not None:
          <tr><td>Vapor pressure:</td>
              <td>{{ "%.1f" % vapor_pres }} hPa</td></tr>
      % end
      % if dew_point is not None:
          <tr><td>Dew point:</td>
              <td>{{ "%.1f" % dew_point }} °C</td></tr>
      % end

      <tr><td colspan=2></td></tr>

      <!-- Pressure -->
      % if pres is not None:
          <tr><td>Pressure:</td>
              <td>{{ pres }} hPa</td></tr>
      % end

      <tr><td colspan=2></td></tr>

      <!-- Wind -->
      % if wnd_speed is not None:
          <tr><td>Wind speed:</td>
              <td>{{ wnd_speed }} m/s </td></tr>
      % end
      % if wnd_dir is not None:
          <tr><td>Wind direction:</td>
              <td>{{ wnd_dir_text }} ({{ wnd_dir }}°)</td></tr>
      % end

      <tr><td colspan=2></td></tr>

      <!-- Rain -->
      <!-- Sensor broken - disabled.
      % if rain_past_day is not None:
          <tr><td>Rain in the last 24 hours:</td>
              <td>{{ "%.2f" % rain_past_day }} mm </td></tr>
      % end

      <tr><td colspan=2></td></tr>
      -->

      <!-- PM 2.5 -->
      % if pm_25 is not None:
          <tr><td>PM 2.5:</td><td>{{ pm_25 }} μg/m³ </td></tr>
      % end
    </table>
    <br/>
    <br/>
    <p>Oldest data:
    {{ "%.0f seconds ago." % data_age if data_age is not None else "unknown." }}
    </p>
    <br/>
    <p>
      Location of the sensors:
      <a href="https://google.com/maps?q=Olsztyn,Poland"
         target="_blank">
        Olsztyn, Poland</a>
    </p>
  </article>

  <article>
    <img src="http://meteo.org.pl/img/ra.png" alt="Current radar map">
    <p>
      Current radar map for the country
    </p>
  </article>
</section>

%include footer
