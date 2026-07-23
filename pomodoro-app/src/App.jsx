import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const App = () => {
  // 定时器状态
  const [timeLeft, setTimeLeft] = useState(25 * 60); // 默认25分钟
  const [isActive, setIsActive] = useState(false);
  const [mode, setMode] = useState('work'); // 'work', 'shortBreak', 'longBreak'
  const [sessionsCompleted, setSessionsCompleted] = useState(0);
  const [sessionsToday, setSessionsToday] = useState(0);
  
  const audioRef = useRef(null);
  
  // 设置时间常量（秒）
  const WORK_TIME = 25 * 60;
  const SHORT_BREAK = 5 * 60;
  const LONG_BREAK = 15 * 60;
  
  // 音效（使用数据URL创建简单提示音）
  const playSound = () => {
    // 创建音频上下文来播放提示音
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800; // 频率
    oscillator.type = 'sine'; // 波形
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 1);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 1);
  };
  
  // 加载今日完成的番茄数
  useEffect(() => {
    const today = new Date().toDateString();
    const stored = localStorage.getItem('pomodoroSessions');
    if (stored) {
      const data = JSON.parse(stored);
      if (data.date === today) {
        setSessionsToday(data.count);
      } else {
        // 如果不是今天，则重置
        localStorage.removeItem('pomodoroSessions');
        setSessionsToday(0);
      }
    }
  }, []);
  
  // 保存今日完成的番茄数
  const saveSessionsToday = (count) => {
    const today = new Date().toDateString();
    localStorage.setItem('pomodoroSessions', JSON.stringify({ date: today, count }));
  };
  
  // 定时器逻辑
  useEffect(() => {
    let interval = null;
    
    if (isActive && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft(timeLeft => timeLeft - 1);
      }, 1000);
    } else if (isActive && timeLeft === 0) {
      // 时间到了，切换模式
      playSound(); // 播放提示音
      
      if (mode === 'work') {
        // 工作时间结束
        const newSessions = sessionsCompleted + 1;
        setSessionsCompleted(newSessions);
        
        // 更新今日统计
        const newTodayCount = sessionsToday + 1;
        setSessionsToday(newTodayCount);
        saveSessionsToday(newTodayCount);
        
        // 判断是否需要长休息
        if (newSessions % 4 === 0) {
          setMode('longBreak');
          setTimeLeft(LONG_BREAK);
        } else {
          setMode('shortBreak');
          setTimeLeft(SHORT_BREAK);
        }
      } else {
        // 休息时间结束，回到工作
        setMode('work');
        setTimeLeft(WORK_TIME);
      }
      
      setIsActive(false);
    }
    
    return () => clearInterval(interval);
  }, [isActive, timeLeft, mode, sessionsCompleted, sessionsToday]);
  
  // 格式化时间为 MM:SS
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };
  
  // 开始/暂停定时器
  const toggleTimer = () => {
    setIsActive(!isActive);
  };
  
  // 重置定时器
  const resetTimer = () => {
    setIsActive(false);
    if (mode === 'work') {
      setTimeLeft(WORK_TIME);
    } else if (mode === 'shortBreak') {
      setTimeLeft(SHORT_BREAK);
    } else {
      setTimeLeft(LONG_BREAK);
    }
  };
  
  // 跳转到下一个模式
  const skipToNext = () => {
    setIsActive(false);
    if (mode === 'work') {
      setMode('shortBreak');
      setTimeLeft(SHORT_BREAK);
    } else if (mode === 'shortBreak') {
      setMode('work');
      setTimeLeft(WORK_TIME);
    } else {
      setMode('work');
      setTimeLeft(WORK_TIME);
    }
  };
  
  // 获取当前模式的颜色和样式
  const getModeStyles = () => {
    switch (mode) {
      case 'work':
        return {
          bg: 'from-red-500 to-orange-500',
          text: 'text-red-100',
          border: 'border-red-400',
          glow: 'shadow-[0_0_30px_rgba(239,68,68,0.4)]'
        };
      case 'shortBreak':
        return {
          bg: 'from-blue-500 to-cyan-500',
          text: 'text-blue-100',
          border: 'border-blue-400',
          glow: 'shadow-[0_0_30px_rgba(59,130,246,0.4)]'
        };
      case 'longBreak':
        return {
          bg: 'from-green-500 to-emerald-500',
          text: 'text-green-100',
          border: 'border-green-400',
          glow: 'shadow-[0_0_30px_rgba(16,185,129,0.4)]'
        };
      default:
        return {
          bg: 'from-gray-500 to-gray-600',
          text: 'text-gray-100',
          border: 'border-gray-400',
          glow: 'shadow-[0_0_30px_rgba(107,114,128,0.4)]'
        };
    }
  };
  
  const modeStyles = getModeStyles();
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center p-4">
      <div className={`w-full max-w-md mx-auto p-8 rounded-3xl bg-gradient-to-br ${modeStyles.bg} text-white shadow-2xl ${modeStyles.glow}`}>
        {/* 标题 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">番茄工作法</h1>
          <p className="text-xl opacity-90">
            {mode === 'work' ? '专注工作' : mode === 'shortBreak' ? '短暂休息' : '长休息'}
          </p>
        </div>
        
        {/* 主要计时器显示 */}
        <div className="text-center mb-8">
          <div className={`text-6xl md:text-7xl font-mono font-bold mb-4 ${modeStyles.text} bg-black/20 py-6 px-8 rounded-2xl border ${modeStyles.border}`}>
            {formatTime(timeLeft)}
          </div>
          
          {/* 会话计数器 */}
          <div className="flex justify-between items-center mt-6 text-lg">
            <div className="text-center">
              <p className="opacity-80">今日番茄</p>
              <p className="text-2xl font-bold">{sessionsToday}</p>
            </div>
            <div className="text-center">
              <p className="opacity-80">累计番茄</p>
              <p className="text-2xl font-bold">{sessionsCompleted}</p>
            </div>
            <div className="text-center">
              <p className="opacity-80">当前轮次</p>
              <p className="text-2xl font-bold">{Math.ceil(sessionsCompleted / 4) + 1}</p>
            </div>
          </div>
        </div>
        
        {/* 控制按钮 */}
        <div className="flex flex-wrap gap-3 justify-center">
          <button
            onClick={toggleTimer}
            className={`px-6 py-3 rounded-xl font-semibold text-lg transition-all duration-200 ${
              isActive 
                ? 'bg-red-500 hover:bg-red-600 transform scale-95' 
                : 'bg-green-500 hover:bg-green-600 transform scale-105'
            }`}
          >
            {isActive ? '暂停' : '开始'}
          </button>
          
          <button
            onClick={resetTimer}
            className="px-6 py-3 bg-yellow-500 hover:bg-yellow-600 rounded-xl font-semibold text-lg transition-all duration-200"
          >
            重置
          </button>
          
          <button
            onClick={skipToNext}
            className="px-6 py-3 bg-purple-500 hover:bg-purple-600 rounded-xl font-semibold text-lg transition-all duration-200"
          >
            跳过
          </button>
        </div>
        
        {/* 模式选择器 */}
        <div className="mt-8 grid grid-cols-3 gap-2">
          <button
            onClick={() => {
              setMode('work');
              setTimeLeft(WORK_TIME);
              setIsActive(false);
            }}
            className={`py-2 px-3 rounded-lg text-sm font-medium transition-all ${
              mode === 'work' 
                ? 'bg-white/20 text-white' 
                : 'bg-black/20 text-white/80 hover:bg-black/30'
            }`}
          >
            工作 (25分)
          </button>
          <button
            onClick={() => {
              setMode('shortBreak');
              setTimeLeft(SHORT_BREAK);
              setIsActive(false);
            }}
            className={`py-2 px-3 rounded-lg text-sm font-medium transition-all ${
              mode === 'shortBreak' 
                ? 'bg-white/20 text-white' 
                : 'bg-black/20 text-white/80 hover:bg-black/30'
            }`}
          >
            短休 (5分)
          </button>
          <button
            onClick={() => {
              setMode('longBreak');
              setTimeLeft(LONG_BREAK);
              setIsActive(false);
            }}
            className={`py-2 px-3 rounded-lg text-sm font-medium transition-all ${
              mode === 'longBreak' 
                ? 'bg-white/20 text-white' 
                : 'bg-black/20 text-white/80 hover:bg-black/30'
            }`}
          >
            长休 (15分)
          </button>
        </div>
        
        {/* 进度指示器 */}
        <div className="mt-6">
          <div className="flex justify-center gap-1">
            {[...Array(4)].map((_, i) => (
              <div
                key={i}
                className={`w-3 h-3 rounded-full ${
                  i < sessionsCompleted % 4 ? 'bg-yellow-400' : 'bg-white/20'
                }`}
              />
            ))}
          </div>
          <p className="text-center text-sm opacity-70 mt-2">
            {sessionsCompleted % 4}/4 完成，{4 - (sessionsCompleted % 4)} 剩余到达长休息
          </p>
        </div>
      </div>
    </div>
  );
};

export default App;