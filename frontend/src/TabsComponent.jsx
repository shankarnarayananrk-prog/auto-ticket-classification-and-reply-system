import React, { useState } from 'react';
import { MessageSquare, Ticket as TicketIcon, MessagesSquare, Clock } from 'lucide-react';

function TabsComponent({ children, activeTab, setActiveTab }) {
  const tabs = [
    { id: 'create', label: 'Create Ticket', icon: TicketIcon },
    { id: 'history', label: 'Tickets', icon: Clock },
    { id: 'messages', label: 'Messages', icon: MessagesSquare }
  ];

  return (
    <div className="tabs-wrapper">
      <div className="tabs-header">
        {tabs.map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <Icon size={18} />
              {tab.label}
            </button>
          );
        })}
      </div>

      <div className="tab-panel">
        {React.Children.map(children, child => {
          if (child.props.tabId === activeTab) {
            return child;
          }
          return null;
        })}
      </div>
    </div>
  );
}

export default TabsComponent;
