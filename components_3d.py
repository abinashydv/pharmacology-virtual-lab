"""
Interactive 3D Molecular Viewer Component using 3Dmol.js
Integrates seamlessly with Streamlit HTML components.
"""

import json

def render_3dmol_viewer(molblock: str, model_type: str = "Ball and Stick", show_surface: bool = False, height: int = 440) -> str:
    """
    Generates interactive HTML containing 3Dmol.js canvas for 3D molecular visualization.
    Supports styles: Ball and Stick, Stick, Space Filling, Wireframe, Cartoon.
    """
    if not molblock:
        return "<div style='color:#ff6b6b; padding:20px; text-align:center;'>No 3D conformer data available.</div>"

    # Escape molblock for JS embedding
    mol_escaped = json.dumps(molblock)

    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
          background-color: #0e1117;
          color: #fafafa;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
          overflow: hidden;
        }}
        #viewer-container {{
          position: relative;
          width: 100%;
          height: {height}px;
          border-radius: 8px;
          border: 1px solid #30363d;
          background: radial-gradient(circle at center, #161b26 0%, #0e1117 100%);
          overflow: hidden;
        }}
        #mol-canvas {{
          width: 100%;
          height: 100%;
        }}
        .controls-toolbar {{
          position: absolute;
          top: 10px;
          right: 10px;
          display: flex;
          gap: 6px;
          z-index: 10;
        }}
        .ctrl-btn {{
          background: rgba(38, 43, 56, 0.85);
          color: #e6edf3;
          border: 1px solid #484f58;
          border-radius: 6px;
          padding: 6px 10px;
          font-size: 11px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
          backdrop-filter: blur(4px);
        }}
        .ctrl-btn:hover {{
          background: #3b82f6;
          border-color: #60a5fa;
          color: #ffffff;
        }}
        .hud-info {{
          position: absolute;
          bottom: 10px;
          left: 12px;
          font-size: 11px;
          color: #8b949e;
          background: rgba(14, 17, 23, 0.7);
          padding: 4px 8px;
          border-radius: 4px;
          pointer-events: none;
        }}
        .atom-tooltip {{
          position: absolute;
          top: 10px;
          left: 12px;
          background: rgba(15, 23, 42, 0.9);
          border: 1px solid #38bdf8;
          color: #38bdf8;
          padding: 4px 10px;
          border-radius: 4px;
          font-size: 11px;
          font-family: monospace;
          display: none;
          pointer-events: none;
        }}
      </style>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.4.2/3Dmol-min.js"></script>
    </head>
    <body>
      <div id="viewer-container">
        <div class="controls-toolbar">
          <button class="ctrl-btn" id="spin-btn" title="Toggle Auto-Spin">🔄 Spin</button>
          <button class="ctrl-btn" id="reset-btn" title="Reset View & Camera">🎯 Reset</button>
        </div>
        <div class="atom-tooltip" id="tooltip"></div>
        <div id="mol-canvas"></div>
        <div class="hud-info">🖱️ Left Drag: Rotate | Scroll: Zoom | Right Drag: Pan</div>
      </div>

      <script>
        (function() {{
          const molData = {mol_escaped};
          const modelType = "{model_type}";
          const showSurface = {str(show_surface).lower()};
          
          let spinning = false;
          let viewer = null;

          function initViewer() {{
            const element = document.getElementById('mol-canvas');
            const config = {{ backgroundColor: '#0e1117' }};
            viewer = $3Dmol.createViewer(element, config);

            // Add model
            viewer.addModel(molData, "mol");

            // Apply selected visualization style
            applyStyle(modelType);

            // Optional van der Waals surface
            if (showSurface) {{
              viewer.addSurface($3Dmol.SurfaceType.VDW, {{
                opacity: 0.55,
                color: '#38bdf8'
              }});
            }}

            // Tooltip on atom hover
            const tooltip = document.getElementById('tooltip');
            viewer.setHoverable({{}}, true,
              function(atom, viewer, event, container) {{
                if (atom) {{
                  tooltip.style.display = 'block';
                  tooltip.innerHTML = '<b>' + (atom.elem || 'Atom') + '</b> (Idx: ' + atom.serial + ')';
                }}
              }},
              function(atom, viewer, event, container) {{
                tooltip.style.display = 'none';
              }}
            );

            viewer.zoomTo();
            viewer.render();
          }}

          function applyStyle(styleName) {{
            if (!viewer) return;
            viewer.setStyle({{}}, {{}}); // Clear existing style

            switch(styleName) {{
              case "Stick":
                viewer.setStyle({{}}, {{ stick: {{ radius: 0.22, colorscheme: 'Jmol' }} }});
                break;
              case "Space Filling":
                viewer.setStyle({{}}, {{ sphere: {{ scale: 0.88, colorscheme: 'Jmol' }} }});
                break;
              case "Wireframe":
                viewer.setStyle({{}}, {{ line: {{ linewidth: 2.2, colorscheme: 'Jmol' }} }});
                break;
              case "Cartoon":
                viewer.setStyle({{}}, {{ cartoon: {{ color: 'spectrum' }}, stick: {{ radius: 0.12, colorscheme: 'Jmol' }} }});
                break;
              case "Ball and Stick":
              default:
                viewer.setStyle({{}}, {{
                  stick: {{ radius: 0.15, colorscheme: 'Jmol' }},
                  sphere: {{ scale: 0.28, colorscheme: 'Jmol' }}
                }});
                break;
            }}
            viewer.render();
          }}

          document.getElementById('spin-btn').addEventListener('click', function() {{
            if (!viewer) return;
            spinning = !spinning;
            if (spinning) {{
              viewer.spin('y', 1.0);
              this.textContent = '⏸ Pause';
              this.style.background = '#22c55e';
            }} else {{
              viewer.spin(false);
              this.textContent = '🔄 Spin';
              this.style.background = 'rgba(38, 43, 56, 0.85)';
            }}
          }});

          document.getElementById('reset-btn').addEventListener('click', function() {{
            if (!viewer) return;
            if (spinning) {{
              viewer.spin(false);
              spinning = false;
              document.getElementById('spin-btn').textContent = '🔄 Spin';
              document.getElementById('spin-btn').style.background = 'rgba(38, 43, 56, 0.85)';
            }}
            viewer.zoomTo();
            viewer.render();
          }});

          window.addEventListener('DOMContentLoaded', initViewer);
          if (document.readyState === 'complete' || document.readyState === 'interactive') {{
            initViewer();
          }}
        }})();
      </script>
    </body>
    </html>
    """
    return html_code
