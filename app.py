<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Public Script Server</title>
  <style>
    :root {
      --accent: #0f9d58;
      --panel: #121212;
      --panel-grad-top: #222;
      --panel-grad-bot: #111;
      --border: 1px solid #333;
      --radius: 12px;
      --shadow: 0 0 10px rgba(0, 0, 0, 0.7);
      --font-mono: monospace;
      --glow: 0 0 6px var(--accent);
    }

    body {
      background: #000;
      color: #eee;
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 0 1rem 2rem;
      min-height: 100vh;
    }

    header {
      max-width: 700px;
      margin: 1rem auto;
      text-align: center;
    }

    main {
      max-width: 700px;
      margin: 0 auto;
    }

    /* === MAXNET Push-to-Talk Radio === */
    .ptt-radio {
      max-width: 600px; margin: 1rem auto 1.25rem; display: grid; grid-template-columns: 1fr auto; gap: 12px; align-items: stretch;
      background: linear-gradient(180deg,var(--panel-grad-top),var(--panel-grad-bot)), var(--panel);
      border: var(--border); border-radius: var(--radius); box-shadow: var(--shadow); padding: .9rem 1rem;
    }
    .ptt-face { display:flex; flex-direction:column; gap:8px; min-width:0; }
    .ptt-title { font-weight:800; letter-spacing:.06em; opacity:.9; }
    .ptt-status { font-family: var(--font-mono); font-size:.9rem; opacity:.8; }
    .ptt-meter { height: 6px; border: 1px solid var(--accent); border-radius: 999px; overflow:hidden; background: rgba(0,0,0,.35); }
    .ptt-level { height: 100%; width: 0%; background: var(--accent); transition: width .08s linear; box-shadow: var(--glow); }
    .ptt-handset { display:flex; align-items:center; justify-content:center; }
    #pttButton { position: relative; width: 120px; height: 120px; border-radius: 18px; border: 2px solid var(--accent); background: #0b0e0f; font-weight: 900; font-size: .95rem; line-height:1.1; text-align:center; box-shadow: var(--shadow); }
    #pttButton:active { transform: translateY(1px); }
    #pttButton .led { position:absolute; top:8px; right:8px; width:10px; height:10px; border-radius:50%; border:1px solid var(--accent); background:#081; box-shadow: 0 0 10px rgba(0,255,0,.6); }
    #pttButton.listening .led { background:#f33; box-shadow: 0 0 10px rgba(255,0,0,.6); }
    .ptt-hint { font-size:.8rem; opacity:.7; text-align:center; margin-top:.25rem; }
    @media (max-width: 600px){ .ptt-radio { grid-template-columns: 1fr; } .ptt-handset{ order:-1; } #pttButton{ width:100%; height:64px; border-radius:10px; } }

    /* --- Mobile-friendly tweaks --- */

    /* Keep Exit button above the flashing overlay in Chaos Mode */
    body.chaos-mode #exitChaosButton {
      position: fixed !important;
      top: 16px;
      right: 16px;
      z-index: 10000; /* higher than #flash (999) and chatbot (9999) */
    }

    /* Additional styling for other UI elements omitted for brevity */
  </style>
</head>
<body>
  <header>
    <h1>Public Script Server</h1>
  </header>

  <main>
    <div id="topButtons">
      <button id="toggleChaos">Toggle Chaos Mode</button>
      <button id="exitChaosButton" style="display:none;">Exit Chaos Mode</button>
    </div>

    <div class="ptt-radio" id="pttRadio">
      <div class="ptt-face">
        <div class="ptt-title">MAXNET Walkie • Push-to-Talk</div>
        <div class="ptt-status" id="pttStatus">Idle — hold to speak</div>
        <div class="ptt-meter"><div class="ptt-level" id="pttLevel" style="width:0%"></div></div>
        <div class="ptt-hint">Hold button or press <kbd>Space</kbd> to talk • Release to send</div>
      </div>
      <div class="ptt-handset">
        <button id="pttButton" aria-label="Hold to talk">
          <span class="led" aria-hidden="true"></span>
          HOLD<br>TO TALK
        </button>
      </div>
    </div>

    <!-- Other page content -->
  </main>

  <script>
    const userInput = document.querySelector('input, textarea');

    // Chaos Mode handlers omitted for brevity

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && document.body.classList.contains('chaos-mode')) {
        document.body.classList.remove('chaos-mode');
        document.getElementById('exitChaosButton').style.display = 'none';
      }
    });

    // === MAXNET Push-to-Talk (Realtime API over WebRTC) ===
    (function(){
      const pttBtn = document.getElementById('pttButton');
      const pttStatus = document.getElementById('pttStatus');
      const pttLevel = document.getElementById('pttLevel');
      if (!pttBtn) return;

      let pc;               // RTCPeerConnection
      let micStream;        // MediaStream from getUserMedia
      let remoteAudio;      // <audio> sink
      let initialized = false;
      let sending = false;
      let dc;               // DataChannel for realtime events

      async function initConnection(){
        if (initialized) return;
        initialized = true;
        // Create audio sink for model output
        remoteAudio = document.createElement('audio');
        remoteAudio.autoplay = true;
        document.body.appendChild(remoteAudio);

        // Prepare mic access
        micStream = await navigator.mediaDevices.getUserMedia({ audio: true });

        pc = new RTCPeerConnection();
        // Play remote audio
        pc.ontrack = (ev)=>{ remoteAudio.srcObject = ev.streams[0]; };

        // Data channel for response control
        dc = pc.createDataChannel('oai-events');
        dc.onopen = () => { /* ready to send events */ };
        dc.onerror = (e) => { console.warn('oai-events error', e); };

        // Create offer expecting to receive audio from model
        const offer = await pc.createOffer({ offerToReceiveAudio: true, offerToReceiveVideo: false });
        await pc.setLocalDescription(offer);

        // Get ephemeral client secret from your server
        const tokenRes = await fetch('/session');
        const { client_secret } = await tokenRes.json();

        const sdpAnswer = await fetch('https://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${client_secret.value}`, 'Content-Type': 'application/sdp' },
          body: offer.sdp
        }).then(r=>r.text());
        await pc.setRemoteDescription({ type:'answer', sdp: sdpAnswer });

        pttStatus.textContent = 'Ready — hold to speak';
      }

      // Simple input level meter
      let audioCtx, analyser, dataArr;
      function ensureMeter(){
        if (audioCtx) return;
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const src = audioCtx.createMediaStreamSource(micStream);
        analyser = audioCtx.createAnalyser(); analyser.fftSize = 256;
        src.connect(analyser); dataArr = new Uint8Array(analyser.frequencyBinCount);
        const tick = ()=>{ if (!analyser) return; analyser.getByteTimeDomainData(dataArr); let max=0; for (let i=0;i<dataArr.length;i++){ const v=Math.abs(dataArr[i]-128); if(v>max) max=v; } const pct=Math.min(100, Math.floor((max/128)*140)); pttLevel.style.width = sending? pct+"%":"0%"; requestAnimationFrame(tick); };
        tick();
      }

      function startTalking(){
        if (!pc || !micStream) return;
        if (sending) return;
        sending = true; pttBtn.classList.add('listening'); pttStatus.textContent = 'Listening… release to send';
        // Attach mic tracks while held
        micStream.getTracks().forEach(t=> pc.addTrack(t, micStream));
        ensureMeter();
      }

      function stopTalking(){
        if (!pc) return; if (!sending) return; sending = false; pttBtn.classList.remove('listening'); pttStatus.textContent = 'Sending…';
        // Remove mic tracks to signal end of utterance
        const senders = pc.getSenders();
        senders.forEach(s=>{ if (s.track && s.track.kind === 'audio') pc.removeTrack(s); });

        // Ask model to create an audio response now
        try {
          if (dc && dc.readyState === 'open') {
            dc.send(JSON.stringify({
              type: 'response.create',
              response: {
                modalities: ['audio'],
                instructions: 'You are MAXNET – a sassy, playful Gen Z assistant. Keep replies short, speak like Max, and respond to the last user utterance you just heard. Use conversational tone and mild sass.'
              }
            }));
          }
        } catch (e) { console.warn('response.create send failed', e); }

        pttStatus.textContent = 'Ready — hold to speak';
      }

      // Init on first interaction for permissions
      pttBtn.addEventListener('pointerdown', async ()=>{ if(!initialized){ await initConnection(); } startTalking(); });
      pttBtn.addEventListener('pointerup', stopTalking);
      pttBtn.addEventListener('pointerleave', stopTalking);
      pttBtn.addEventListener('keydown', (e)=>{ if(e.code==='Space'){ e.preventDefault(); startTalking(); }});
      pttBtn.addEventListener('keyup',   (e)=>{ if(e.code==='Space'){ e.preventDefault(); stopTalking();  }});

      // Global Spacebar shortcut when button is visible
      document.addEventListener('keydown', (e)=>{ if(e.code==='Space' && document.activeElement!==userInput){ e.preventDefault(); if(!initialized){ initConnection(); } startTalking(); }});
      document.addEventListener('keyup',   (e)=>{ if(e.code==='Space' && document.activeElement!==userInput){ e.preventDefault(); stopTalking(); }});
    })();
  </script>
</body>
</html>
