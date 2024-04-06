import React, { useEffect, useRef } from 'react';
import { Terminal as XTerm } from '@xterm/xterm';
import '@xterm/xterm/css/xterm.css';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';

const Terminal = () => {
  const terminalRef = useRef();
	const navigate = useNavigate()
	let socket = null;

  useEffect(() => {
		const terminal = new XTerm({
			cols: 80
		})
		const token = Cookies.get('session_token')
		if (!token) {
			navigate('/login')
		}

		try {
			terminal.open(terminalRef.current);
			socket = new WebSocket(`ws://localhost:8000/ws/stream?token=${token}`)

			socket.onopen = () => {
				console.log('websocket connected')
				socket.onmessage = (event) => {
					terminal.write(event.data)
				}
			}
			socket.onerror = (error) => {
				console.log('Websocket error: ', error)
			}

			terminal.onKey((event) => {
					socket.send(JSON.stringify({ event: "shellstream", command: event.key }))
			})
			terminal.focus()
		} catch (error) {
			Cookies.remove('session_token')
			console.log('Error: ', error)
		}

    return () => {
			socket.close()
      terminal.dispose();
    }
  }, [])

  return (
		<div className='flex overflow-hidden justify-center items-center w-screen h-screen'>
			<div ref={terminalRef} />
		</div>
		)
};

export default Terminal;
