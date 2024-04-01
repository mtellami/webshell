import React, { useEffect, useRef } from 'react';
import { Terminal as XTerm } from '@xterm/xterm';
import '@xterm/xterm/css/xterm.css';

const Terminal = () => {
  const terminalRef = useRef();
	let socket;

  useEffect(() => {
    const terminal = new XTerm();
    terminal.open(terminalRef.current);
		try {
			socket = new WebSocket('ws://localhost:8000/ws/stream')
			socket.onopen = (event) => {
				console.log('websocket connected')
				socket.send(JSON.stringify({ event: "shellstream", command: "ls -l" }))
				socket.onmessage = (event) => {
					console.log(event)
					terminal.write(event.data)
				}
			}
			socket.onerror = (error) => {
				console.log('Websocket error: ', error)
			}
		} catch (error) {
			console.log('Error: ', error)
		}

    terminal.write('Welcome to xterm.js\n\r');
    
    return () => {
			socket.close()
      terminal.dispose();
    };
  }, []);

  return (
		<>
			<div ref={terminalRef} />
			<input type='text' id='test' />
			<button onClick={(event) => socket.send(JSON.stringify({ event: "shellstream", command: document.getElementById('test')?.value }))}>
				click
			</button>
		</>
	)
};

export default Terminal;
