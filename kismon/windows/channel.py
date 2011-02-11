import gtk

class ChannelWindow:
	def __init__(self, sources, client):
		self.sources = sources
		self.client = client
		self.changes = {}
		self.widgets = {}
		
		self.gtkwin = gtk.Window()
		self.gtkwin.set_position(gtk.WIN_POS_CENTER)
		self.gtkwin.set_default_size(320, 240)
		self.gtkwin.set_title("Configure Channel")
		
		vbox = gtk.VBox()
		self.gtkwin.add(vbox)
		
		self.sources_list = gtk.VBox()
		sources_list_scroll = gtk.ScrolledWindow()
		sources_list_scroll.add_with_viewport(self.sources_list)
		sources_list_scroll.get_children()[0].set_shadow_type(gtk.SHADOW_NONE)
		sources_list_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sources_list_scroll, expand=True, fill=True)
		
		for uuid in self.sources:
			self.widgets[uuid] = {}
			source = self.sources[uuid]
			frame = gtk.Frame(source["username"])
			self.sources_list.pack_start(frame, expand=False, fill=False)
			
			table = gtk.Table(3, 3)
			frame.add(table)
			hop_button = gtk.RadioButton(None, 'Hop')
			if source["hop"] == 1:
				hop_button.clicked()
			hop_button.connect("clicked", self.on_change_mode, uuid, "hop")
			hop_button.set_alignment(0,0)
			table.attach(hop_button, 0, 1, 0, 1)
			
			field = gtk.SpinButton()
			field.set_numeric(True)
			field.set_max_length(3)
			field.set_increments(1,10)
			field.set_range(1,100)
			if source["hop"] == 1:
				field.set_value(source["velocity"])
			else:
				field.set_value(3)
				field.set_sensitive(False)
			self.widgets[uuid]["hop"] = field
			field.connect("changed", self.on_change_value, uuid, "hop")
			table.attach(field, 1, 2, 0, 1, xoptions=gtk.SHRINK)
			
			label = gtk.Label("rate")
			label.set_justify(gtk.JUSTIFY_LEFT)
			label.set_alignment(0.1,0.5)
			table.attach(label, 2, 3, 0, 1, xoptions=gtk.FILL)
			
			lock_button = gtk.RadioButton(hop_button, "Lock")
			if source["hop"] == 0:
				lock_button.clicked()
			lock_button.connect("clicked", self.on_change_mode, uuid, "lock")
			hop_button.set_alignment(0,0)
			table.attach(lock_button, 0, 1, 1, 2)
			
			field = gtk.SpinButton()
			field.set_numeric(True)
			field.set_max_length(3)
			field.set_increments(1,10)
			field.set_range(1,100)
			if source["hop"] == 0:
				field.set_value(source["channel"])
			else:
				field.set_value(1)
				field.set_sensitive(False)
			
			self.widgets[uuid]["lock"] = field
			field.connect("changed", self.on_change_value, uuid, "lock")
			table.attach(field, 1, 2, 1, 2, xoptions=gtk.SHRINK)
			
			label = gtk.Label("channel")
			label.set_justify(gtk.JUSTIFY_FILL)
			label.set_alignment(0.1,0.5)
			table.attach(label, 2, 3, 1, 2, xoptions=gtk.FILL)
			
		button_box = gtk.HButtonBox()
		vbox.pack_end(button_box, expand=False, fill=False)
		
		cancel_button = gtk.Button(stock=gtk.STOCK_CANCEL)
		cancel_button.connect("clicked", self.on_cancel)
		button_box.add(cancel_button)
		
		apply_button = gtk.Button(stock=gtk.STOCK_APPLY)
		apply_button.connect("clicked", self.on_apply)
		button_box.add(apply_button)
		
		self.gtkwin.show_all()
		
	def on_change_mode(self, widget, uuid, mode):
		if not widget.get_active():
			return
		
		self.changes[uuid] = mode
		self.widgets[uuid][mode].set_sensitive(True)
		if mode == "lock":
			self.widgets[uuid]["hop"].set_sensitive(False)
		else:
			self.widgets[uuid]["lock"].set_sensitive(False)
		
	def on_change_value(self, widget, uuid, mode):
		self.changes[uuid] = mode
		
	def on_apply(self, widget):
		for uuid in self.changes:
			mode = self.changes[uuid]
			value = int(self.widgets[uuid][mode].get_value())
			self.client.set_channel(uuid, mode, value)
		
		self.gtkwin.destroy()
		
	def on_cancel(self, widget):
		self.gtkwin.destroy()