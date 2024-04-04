import React, { useEffect, useRef, useState } from 'react';
import { Terminal as XTerm } from '@xterm/xterm';
import '@xterm/xterm/css/xterm.css';

const Terminal = () => {
  const terminalRef = useRef();
	let socket = null;
	let input = ''

  useEffect(() => {
		const terminal = new XTerm();
		try {
			terminal.open(terminalRef.current);
			socket = new WebSocket('ws://localhost:8000/ws/stream')

			socket.onopen = () => {
				console.log('websocket connected')
				// socket.send(JSON.stringify({ event: "shellstream", command: input }))
				socket.onmessage = (event) => {
					terminal.write(event.data)
					input = ''
				}
			}
			socket.onerror = (error) => {
				console.log('Websocket error: ', error)
			}

			terminal.onKey((event) => {
				if (event.key.charCodeAt(0) >= 32 && event.key.charCodeAt(0) <= 126) {
					input += event.key
					terminal.write(event.key)
				} else if (event.key == '\r') {
					socket.send(JSON.stringify({ event: "shellstream", command: input }))
				} else if (event.key.charCodeAt(0) == 127 && input !== '') {
					terminal.write('\b \b')
					input = input.slice(0, input.length - 1)
				}
			})

			terminal.focus()
		} catch (error) {
			console.log('Error: ', error)
		}

    return () => {
			socket.close()
      terminal.dispose();
    }
  }, [])

  return <div ref={terminalRef} />
};

export default Terminal;
