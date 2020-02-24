/* 
 Assumptions:
    1. Bridge names are in the format: B1, B2, ..., BN;
    2. Lan names are single characters.
	3. System is considered stabilized after 25 units of time.
*/

#include<bits/stdc++.h>
using namespace std;

class Bridge {
	public:
		struct config_message {
			int root_id, root_path_cost, bridge_id;
			char port_id;
			config_message() : root_id(INT_MAX), root_path_cost(INT_MAX),  bridge_id(INT_MAX), port_id(CHAR_MAX) {};
			config_message(int root_id, int root_path_cost, int bridge_id, char port_id) : root_id(root_id), root_path_cost(root_path_cost), bridge_id(bridge_id), port_id(port_id) {};
			bool operator<(const config_message &other) const{
				if (root_id != other.root_id) return root_id < other.root_id;
				else if (root_path_cost != other.root_path_cost) return root_path_cost < other.root_path_cost;
				else if (bridge_id != other.bridge_id) return bridge_id < other.bridge_id;
				else if (port_id != other.port_id) return port_id < other.port_id;
				else return false;
			};
		};

		struct port {
			char port_id;
			config_message best_received_config_message;
			port(char port_id): port_id(port_id), best_received_config_message(config_message()) {}
			port(char port_id, config_message best_received_config_message): port_id(port_id), best_received_config_message(best_received_config_message) {}
			bool operator<(const port &other) const {
				if (port_id != other.port_id) 
					return port_id < other.port_id;
				return best_received_config_message < other.best_received_config_message;
			};
		};
	
		Bridge(int id): root_id(id), root_path_cost(0), id(id), root_port_id(0) {
			best_received_config_message = config_message(id, -1, INT_MAX, 0);
		}

		void add_adjacent(char port_id) {
			this->adjacent_ports.insert(port(port_id));
		}

		void update_on_receive(int time) {
			for (auto config_message_iterator = received_config_message.begin(); config_message_iterator != received_config_message.end(); config_message_iterator++) {
				auto config_msg = *config_message_iterator;
				if (config_msg.first == time) {
					auto config = config_msg.second;
					auto port_iterator = get_port(config.port_id);
					if (config < port_iterator->best_received_config_message) {
						adjacent_ports.erase(port_iterator);
						adjacent_ports.insert(port(config.port_id, config));
					}
					if (config < this->best_received_config_message)
						this->update_status(config);
					received_config_message.erase(config_message_iterator);

					cout << "At t = " << time << " Bridge B" << id << " receives (B" << config.root_id << ", " << config.root_path_cost << ", B" << config.bridge_id << ")\n";
				}
			}
		}

		set< pair<int, config_message> > generate_config_message(int time) const {
			set< pair<int, config_message> > generated_config_message;
			bool atleast_one_insertion = false;
			for (const char &designated_port_id: this->provide_designated_ports()) {
				generated_config_message.insert(make_pair(time + 1, this->get_config_message(designated_port_id)));
				atleast_one_insertion = true;
			}
			if (atleast_one_insertion) cout << "At t = " << time << " Bridge B" << id << " sends (B" << root_id << ", " << root_path_cost << ", B" << id << ")\n";
			return generated_config_message;
		}

		void insert_configration_message(pair<int, config_message> config_message) {
			received_config_message.insert(config_message);
		}

		void print_current_config() const {
			auto designated_ports = this->provide_designated_ports();
			bool can_be_closed = designated_ports.size() == 0;
			cout << 'B' << id << ": ";
			if (can_be_closed){
				cout << "All ports closed." << endl;
				return;
			}
			for (const auto &port: adjacent_ports) {
				string port_status;
				if (designated_ports.find(port.port_id) != designated_ports.end()) port_status = "Designated.";
				else if (port.port_id == root_port_id) port_status = "Active";
				else port_status = "Closed";
				cout << port.port_id << '-' << port_status << ' ';
			}
			cout << endl;
		}

	private:
		int root_id, root_path_cost, id; 
		char root_port_id;
		config_message best_received_config_message;
		set<port> adjacent_ports;
		set< pair<int, config_message> > received_config_message;
		
		void update_status(config_message config_message) {
			best_received_config_message = config_message;
			root_id = best_received_config_message.root_id;
			root_path_cost = best_received_config_message.root_path_cost + 1;
			root_port_id = best_received_config_message.port_id;
		}

		config_message get_config_message(char port_id) const {
			return config_message(root_id, root_path_cost, id, port_id);
		}

		set<port>::iterator get_port(char port_id) const {
			return find_if(this->adjacent_ports.begin(), this->adjacent_ports.end(), [&port_id](Bridge::port port) {return port.port_id == port_id;});
		}

		set<char> provide_designated_ports() const {
			set<char> designated_ports;
			for (auto &port: this->adjacent_ports) {
				if (this->get_config_message(port.port_id) < port.best_received_config_message) {
					designated_ports.insert(port.port_id);
				}
			}
			return designated_ports;
		}
};

void take_input(int num_of_bridges, vector<Bridge> &network, map <char, vector<int>> &lan_to_bridges) {

	cout << "Provide entries in the format BX: Lan1 Lan2 Lan3 (where BX is bridge id and in format B1, B2, ... and Lan1, Lan2, ... are lan names and in format A, B, C, D etc)." << endl;
	network.reserve(num_of_bridges+1);
	network.push_back(Bridge(0));
	for (int bridge_num = 1; bridge_num <= num_of_bridges; bridge_num++){
		network.push_back(Bridge(bridge_num));
	}
	cin.ignore();

	for (int i = 0; i < num_of_bridges; i++) {
		string line, input_word;
		getline(cin, line);
		istringstream iss(line);
		bool first = true; 
		int bridge_num;
		while (iss >> input_word) {
			if (first) {
				bridge_num = stoi(input_word.substr(1, input_word.length()-2));
				first = false;
			}
			else {
				network[bridge_num].add_adjacent(input_word[0]);
				lan_to_bridges[input_word[0]].push_back(bridge_num);
			}
		}
	}

	for (auto &lan: lan_to_bridges) {
		sort(lan.second.begin(), lan.second.end());
	}
}

void create_spanning_tree(vector<Bridge> &network, map< char, vector<int> > &lan_to_bridges) {

	int num_of_bridges = network.size() - 1;
	for (int time = 1; time <= 10; time++){
		for (int bridge_num = 1; bridge_num <= num_of_bridges; bridge_num++) {
			network[bridge_num].update_on_receive(time);
		}
		for (int bridge_num = 1; bridge_num <= num_of_bridges; bridge_num++) {
			auto generated_messages =  network[bridge_num].generate_config_message(time);
			for (auto const &message: generated_messages) {
				auto config_message = message.second;
				for (const int &receiver_bridge_num: lan_to_bridges[config_message.port_id]) {
					if (receiver_bridge_num != bridge_num) {
						network[receiver_bridge_num].insert_configration_message(message);
					}
				}
			}
		}
	}
	cout << "After system stabilization: " << endl;
	for (int bridge_num = 1; bridge_num <= num_of_bridges; bridge_num++) {
		auto bridge = network[bridge_num];
		bridge.print_current_config();
	}
}

int main() {
	int num_of_bridges;
	cout << "Enter number of bridges in the network: ";
	cin >> num_of_bridges;
	vector <Bridge> network;
	map <char, vector<int>> lan_to_bridges;
	take_input(num_of_bridges, network, lan_to_bridges);
	create_spanning_tree(network, lan_to_bridges);
}