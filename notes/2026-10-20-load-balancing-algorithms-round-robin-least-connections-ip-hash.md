# Load Balancing Algorithms (Round Robin, Least Connections, IP Hash)

## Overview

In the world of modern applications, especially those dealing with high traffic or complex computations like machine learning model serving, a single server often isn't enough to handle all requests efficiently. This is where **Load Balancing** comes into play. Load balancing is the process of distributing network traffic across multiple servers, known as a server farm or cluster. The primary goal is to optimize resource utilization, maximize throughput, minimize response time, and avoid overloading any single server. It also enhances reliability and availability by providing redundancy; if one server fails, the load balancer can redirect traffic to the remaining healthy servers.

Load balancing algorithms are the rules or methods that a load balancer uses to decide which server should receive an incoming request. This study note will dive into three fundamental and widely used load balancing algorithms:

1.  **Round Robin**: A simple, sequential distribution method.
2.  **Least Connections**: A dynamic method that considers the current workload of servers.
3.  **IP Hash**: A method that ensures a client consistently connects to the same server.

Understanding these algorithms is crucial for anyone involved in designing, deploying, or managing scalable and robust distributed systems, including those powering machine learning inference services.

## What Problem It Solves

Load balancing algorithms address several critical problems and challenges inherent in distributed systems and high-traffic applications:

*   **Single Point of Failure**: Without load balancing, if an application runs on a single server and that server fails, the entire application becomes unavailable. Load balancing distributes traffic across multiple servers, so if one server goes down, the others can continue to handle requests, ensuring high availability and fault tolerance.
*   **Server Overload and Performance Degradation**: A single server has finite resources (CPU, memory, network bandwidth). As traffic increases, a single server can become overwhelmed, leading to slow response times, timeouts, and even crashes. Load balancing prevents this by distributing the load, ensuring no single server is overworked and maintaining optimal performance.
*   **Inefficient Resource Utilization**: In a system with multiple servers, some servers might be idle or underutilized while others are struggling. Load balancing ensures that resources are used efficiently across the entire server pool, maximizing the return on hardware investment.
*   **Scalability Challenges**: As an application grows and user demand increases, it needs to scale. Load balancing makes it easy to add more servers to the backend pool without reconfiguring the entire system. The load balancer automatically starts distributing traffic to the new servers, allowing for seamless horizontal scaling.
*   **Session Management and Statefulness**: For applications that require users to maintain a "session" (e.g., a shopping cart, a logged-in state), it's often important that a user's requests are consistently routed to the same server. Load balancing algorithms like IP Hash specifically address this need, preventing data inconsistencies or loss of session state.

**Why is it needed in machine learning?**

Machine learning models, especially deep learning models, can be computationally intensive during inference (prediction). When deploying these models for real-time applications (e.g., recommendation systems, fraud detection, image recognition), they often need to handle a high volume of prediction requests with low latency.

*   **High Throughput Inference**: A single ML model server might not be able to handle thousands or millions of prediction requests per second. Load balancing allows multiple instances of the model to run on different servers, distributing the inference workload and achieving high throughput.
*   **Low Latency**: By distributing requests, load balancers can help reduce queueing delays on individual servers, leading to faster prediction times for users.
*   **Resource Optimization**: Different ML models or different types of inference requests might have varying computational demands. Load balancing can help ensure that servers are not idle while others are struggling, especially with dynamic algorithms like Least Connections.
*   **A/B Testing and Canary Deployments**: Load balancers are crucial for directing a percentage of traffic to new model versions for A/B testing or gradual rollout (canary deployments) without impacting all users.
*   **Fault Tolerance for ML Services**: If one ML inference server crashes, the load balancer can redirect requests to other healthy servers, ensuring continuous availability of the prediction service.

## How It Works

Let's break down the step-by-step mechanism of each algorithm.

### 1. Round Robin

The Round Robin algorithm is the simplest and most straightforward load balancing method. It distributes incoming client requests to a list of servers in a sequential, rotating manner.

**Mechanism:**

1.  **Maintain a List**: The load balancer maintains an ordered list of available backend servers.
2.  **Sequential Distribution**: When a new request arrives, the load balancer sends it to the first server in its list.
3.  **Advance Pointer**: For the next request, it moves to the next server in the list.
4.  **Cycle Back**: Once it reaches the end of the list, it cycles back to the beginning.

**Example Flow:**
If you have servers S1, S2, S3:
*   Request 1 -> S1
*   Request 2 -> S2
*   Request 3 -> S3
*   Request 4 -> S1 (cycles back)
*   Request 5 -> S2
*   ...and so on.

### 2. Least Connections

The Least Connections algorithm is a dynamic load balancing method that takes into account the current workload of each server. It directs new client requests to the server that currently has the fewest active connections.

**Mechanism:**

1.  **Track Active Connections**: The load balancer continuously monitors and keeps a count of the number of active connections each backend server is currently handling.
2.  **Identify Least Loaded**: When a new request arrives, the load balancer queries its internal state to find the server with the lowest number of active connections.
3.  **Direct Request**: The new request is then sent to that identified server.
4.  **Update Count**: The active connection count for that server is incremented. When a connection closes, the count is decremented.

**Example Flow:**
Servers S1, S2, S3 initially have 0 active connections.
*   Request 1 arrives. All 0. Send to S1. S1 connections: 1. (S1:1, S2:0, S3:0)
*   Request 2 arrives. S2 and S3 have 0. Send to S2. S2 connections: 1. (S1:1, S2:1, S3:0)
*   Request 3 arrives. S3 has 0. Send to S3. S3 connections: 1. (S1:1, S2:1, S3:1)
*   Request 4 arrives. All have 1. Send to S1 (or S2/S3, depending on tie-breaking). S1 connections: 2. (S1:2, S2:1, S3:1)
*   Suppose a connection to S2 closes. S2 connections: 0. (S1:2, S2:0, S3:1)
*   Request 5 arrives. S2 has 0. Send to S2. S2 connections: 1. (S1:2, S2:1, S3:1)

### 3. IP Hash

The IP Hash algorithm ensures that requests from a particular client (identified by their IP address) are always directed to the same backend server. This is crucial for maintaining "sticky sessions" or "session persistence."

**Mechanism:**

1.  **Extract Client IP**: When a new request arrives, the load balancer extracts the client's source IP address.
2.  **Apply Hash Function**: It then applies a hash function to this IP address. A hash function takes an input (the IP address) and returns a fixed-size string of characters or an integer, which is often used as an index.
3.  **Map to Server**: The result of the hash function is used to determine which server in the backend pool should handle the request. Typically, the hash value is taken modulo the number of available servers to get a server index.
4.  **Consistent Routing**: Because the hash of a given IP address will always be the same, subsequent requests from the same client IP will consistently be routed to the same server.

**Example Flow:**
Servers S1, S2, S3. Number of servers $N=3$.
*   Client A (IP: 192.168.1.10) sends a request.
    *   `hash("192.168.1.10")` might result in, say, `12345`.
    *   `12345 % 3 = 0`. So, Request from Client A -> S1 (index 0).
*   Client B (IP: 192.168.1.20) sends a request.
    *   `hash("192.168.1.20")` might result in, say, `67890`.
    *   `67890 % 3 = 0`. So, Request from Client B -> S1 (index 0).
*   Client C (IP: 192.168.1.30) sends a request.
    *   `hash("192.168.1.30")` might result in, say, `11223`.
    *   `11223 % 3 = 2`. So, Request from Client C -> S3 (index 2).
*   Later, Client A sends another request. The hash will still be `12345`, modulo 3 will still be `0`, so it goes to S1.

## Mathematical Intuition

The mathematical intuition behind these algorithms is relatively simple, relying on basic arithmetic and hashing.

### Round Robin

The core idea of Round Robin is sequential iteration with a wrap-around. If we have $N$ servers, indexed from $0$ to $N-1$, and the current server index is $i$, the next server index $i'$ is determined by:

$$i' = (i + 1) \pmod N$$

Where:
*   $i$ is the index of the server that handled the previous request.
*   $N$ is the total number of active servers.
*   $\pmod N$ is the modulo operator, which gives the remainder after division by $N$. This ensures that the index wraps around to $0$ after reaching $N-1$.

For example, if $N=3$ (servers S0, S1, S2):
*   If current $i=0$, next $i' = (0+1) \pmod 3 = 1$ (S1).
*   If current $i=1$, next $i' = (1+1) \pmod 3 = 2$ (S2).
*   If current $i=2$, next $i' = (2+1) \pmod 3 = 0$ (S0, wraps around).

This ensures an even distribution of requests over time, assuming all requests are of similar processing cost and all servers have similar capacity.

### Least Connections

The Least Connections algorithm relies on tracking a state variable for each server and then performing a minimization operation.

Let $C_j$ be the number of active connections on server $j$. If we have $N$ servers, $S_0, S_1, \dots, S_{N-1}$, the load balancer's task is to find the server $S_k$ such that:

$$k = \arg\min_{j \in \{0, \dots, N-1\}} (C_j)$$

Where:
*   $\arg\min$ returns the index $k$ of the server that has the minimum number of active connections.
*   $C_j$ is dynamically updated:
    *   When a new connection is established to server $S_j$, $C_j \leftarrow C_j + 1$.
    *   When a connection to server $S_j$ is terminated, $C_j \leftarrow C_j - 1$.

In case of a tie (multiple servers have the same minimum number of connections), a secondary tie-breaking rule might be applied, such as Round Robin among the tied servers, or choosing the server with the lowest index.

### IP Hash

The IP Hash algorithm uses a hash function to map a client's IP address to a specific server.

Let $IP_{client}$ be the source IP address of the client.
Let $H$ be a hash function that takes $IP_{client}$ as input and produces an integer hash value.
Let $N$ be the total number of active servers.

The server index $k$ for a given client is determined by:

$$k = H(IP_{client}) \pmod N$$

Where:
*   $H(IP_{client})$ is the integer hash value generated from the client's IP address. A common hash function for IP addresses might involve converting the IP address into an integer and then applying a standard hashing algorithm.
*   $\pmod N$ ensures that the resulting server index falls within the range $[0, N-1]$.

The key property here is that for a given $IP_{client}$, $H(IP_{client})$ will always produce the same hash value, and thus $k$ will always be the same, ensuring that the client is consistently routed to the same server. The quality of the hash function is important; it should distribute different IP addresses as evenly as possible across the range of possible hash values to avoid uneven server distribution.

## Advantages

### Round Robin
*   **Simplicity**: Extremely easy to implement and understand.
*   **Even Distribution (for uniform requests)**: Provides a fair and even distribution of requests across servers if all requests are similar in processing time and all servers have equal capacity.
*   **No State Tracking**: The load balancer doesn't need to maintain complex state information about server loads or connections, making it lightweight.

### Least Connections
*   **Dynamic Load Awareness**: Distributes requests based on the actual current workload of each server, leading to better resource utilization.
*   **Handles Heterogeneous Servers**: More effective than Round Robin when servers have different processing capacities or when requests vary significantly in their processing demands.
*   **Prevents Overload**: Actively avoids sending new requests to already busy servers, reducing the chance of server overload and improving overall response times.

### IP Hash
*   **Session Persistence (Sticky Sessions)**: Guarantees that a client's requests are always routed to the same server, which is crucial for stateful applications (e.g., shopping carts, user logins) where session data is stored on the server.
*   **No Server State Tracking (for load balancer)**: Once the hash is computed, the load balancer doesn't need to track active connections or server load, simplifying its internal logic for routing.
*   **Cache Efficiency**: Can improve cache hit rates on individual servers if clients frequently request the same data, as their requests consistently go to the same server.

## Disadvantages

### Round Robin
*   **No Load Awareness**: Does not consider the actual load or capacity of individual servers. A slow or overloaded server will still receive its turn in the rotation, potentially leading to performance bottlenecks.
*   **Inefficient for Heterogeneous Workloads**: If requests vary greatly in processing time, or if servers have different capacities, some servers can become overloaded while others are underutilized.
*   **No Session Persistence**: A client's requests might be routed to different servers over time, which can break stateful applications unless session data is shared across all servers (e.g., using a distributed cache or database).

### Least Connections
*   **Requires State Tracking**: The load balancer needs to continuously monitor and maintain the number of active connections for each server, adding complexity and overhead to the load balancer itself.
*   **Assumes Equal Connection Weight**: It assumes that all active connections represent an equal amount of load. In reality, some connections might be very lightweight (e.g., a static file request) while others are very heavy (e.g., a complex database query or an ML inference request), leading to an inaccurate representation of server load.
*   **Potential for Imbalance with Long-Lived Connections**: If a server receives a few very long-lived connections, it might appear "busy" even if it has capacity for short, bursty requests, leading to other servers being overutilized.

### IP Hash
*   **Uneven Distribution**: If client IP addresses are not diverse (e.g., many clients behind a single NAT gateway sharing an IP), or if the hash function is poor, it can lead to an uneven distribution of load, creating "hot spots" on certain servers.
*   **Server Failure Impact**: If a server fails, all clients that were hashed to that specific server will lose their session and be unable to connect until the server is restored or the load balancer reconfigures its server pool (which might re-hash clients to different servers, breaking existing sessions).
*   **Reduced Flexibility**: Adding or removing servers from the pool can change the modulo operation, potentially re-hashing all clients to different servers and breaking existing sticky sessions. This makes dynamic scaling more challenging.

## Real World Applications

Load balancing algorithms are fundamental to the operation of almost all large-scale distributed systems. Here are 3-5 concrete real-world use cases:

1.  **Web Servers and APIs (e.g., Nginx, Apache, Cloud Load Balancers)**:
    *   **Use Case**: Distributing incoming HTTP/HTTPS requests to multiple backend web servers or API instances.
    *   **Algorithms**:
        *   **Round Robin** is often used for simple, stateless APIs or static content serving where requests are generally uniform.
        *   **Least Connections** is preferred for dynamic web applications or APIs where request processing times can vary, ensuring that busy servers aren't overwhelmed.
        *   **IP Hash** is critical for applications requiring session persistence, such as e-commerce sites (shopping carts), online banking, or user authentication flows, where a user needs to stay connected to the same server throughout their session.
    *   **Example**: A large e-commerce website uses a load balancer to distribute millions of user requests to hundreds of web servers. IP Hash ensures that a user adding items to their cart consistently interacts with the same server instance, maintaining their session state.

2.  **Microservices Architectures**:
    *   **Use Case**: In a microservices environment, applications are broken down into many smaller, independent services. Load balancers (often called API Gateways or Service Meshes) route requests to different instances of these services.
    *   **Algorithms**:
        *   **Least Connections** is very common here because different microservices might have varying loads, and instances of the same service might be processing different types of requests.
        *   **Round Robin** can be used for simpler, stateless microservices.
    *   **Example**: A streaming service might have microservices for user authentication, content recommendation, video transcoding, and billing. A load balancer ensures that requests for the recommendation service are distributed across multiple instances of that service, preventing any single instance from becoming a bottleneck.

3.  **Machine Learning Model Serving**:
    *   **Use Case**: Deploying trained machine learning models as API endpoints for real-time inference. These services need to handle high volumes of prediction requests with low latency.
    *   **Algorithms**:
        *   **Least Connections** is highly beneficial here. Inference requests can vary significantly in computational cost (e.g., a simple classification vs. a complex image generation). Least Connections ensures that requests are sent to the least busy model server, optimizing throughput and latency.
        *   **Round Robin** could be used if all inference requests are known to have very similar processing times.
        *   **IP Hash** might be used if a specific client needs to consistently interact with the same model server instance, perhaps for personalized model updates or stateful inference.
    *   **Example**: A fraud detection system uses an ML model to score transactions in real-time. Multiple instances of the model are deployed. A load balancer using Least Connections ensures that incoming transaction requests are routed to the model server instance that is currently least busy, minimizing the time taken to flag potential fraud.

4.  **Database Clusters (Read Replicas)**:
    *   **Use Case**: Distributing read queries across multiple replica databases to reduce the load on the primary database and improve read performance.
    *   **Algorithms**:
        *   **Round Robin** or **Least Connections** are typically used for read replicas. Round Robin offers simple distribution, while Least Connections can be more effective if some read queries are much heavier than others.
    *   **Example**: A social media platform has a primary database for writes and several read replicas. A load balancer distributes all incoming read requests (e.g., fetching user profiles, news feeds) across these replicas, ensuring that no single replica is overwhelmed and read operations remain fast.

5.  **Content Delivery Networks (CDNs)**:
    *   **Use Case**: Directing users to the closest or least loaded edge server to deliver static content (images, videos, CSS, JavaScript) quickly.
    *   **Algorithms**: While CDNs use more sophisticated algorithms often incorporating geographical location and network latency, the underlying principles of distributing load are similar.
        *   **Least Connections** (or a variant like "least traffic" or "least response time") is often a component to ensure that the chosen edge server is not currently overloaded.
        *   **IP Hash** could be used in specific scenarios where a user's requests for certain content should consistently hit the same cache server.
    *   **Example**: When you access a website, images and videos might be served from a CDN. The CDN's load balancing system directs your request to an edge server geographically close to you and capable of serving the content quickly, often considering its current load.

## Python Example

This Python example demonstrates the three load balancing algorithms by simulating client requests and server responses. We'll create a `Server` class to represent our backend servers and a `LoadBalancer` class that can switch between the different algorithms.

```python
import time
import random
import hashlib

# --- Server Class ---
class Server:
    """Represents a backend server that can handle requests."""
    def __init__(self, server_id, capacity=10):
        self.server_id = server_id
        self.active_connections = 0
        self.requests_handled = 0
        self.capacity = capacity # Max active connections
        self.is_healthy = True
        print(f"Server {self.server_id} initialized with capacity {self.capacity}.")

    def handle_request(self, request_id):
        """Simulates handling a request. Increments connections and requests handled."""
        if not self.is_healthy:
            print(f"Server {self.server_id} is unhealthy, cannot handle request {request_id}.")
            return False

        if self.active_connections >= self.capacity:
            print(f"Server {self.server_id} is at full capacity ({self.active_connections}/{self.capacity}). Request {request_id} rejected.")
            return False

        self.active_connections += 1
        self.requests_handled += 1
        # print(f"Server {self.server_id} handling request {request_id}. Active connections: {self.active_connections}")
        return True

    def finish_request(self, request_id):
        """Simulates a request finishing. Decrements active connections."""
        if self.active_connections > 0:
            self.active_connections -= 1
            # print(f"Server {self.server_id} finished request {request_id}. Active connections: {self.active_connections}")
        else:
            pass # print(f"Warning: Server {self.server_id} tried to finish request {request_id} but no active connections.")

    def set_health(self, is_healthy):
        """Sets the health status of the server."""
        self.is_healthy = is_healthy
        status = "healthy" if is_healthy else "unhealthy"
        print(f"Server {self.server_id} is now {status}.")

    def __str__(self):
        return (f"Server {self.server_id} (Connections: {self.active_connections}/{self.capacity}, "
                f"Handled: {self.requests_handled}, Healthy: {self.is_healthy})")

# --- Load Balancer Class ---
class LoadBalancer:
    """
    Simulates a Load Balancer with Round Robin, Least Connections, and IP Hash algorithms.
    """
    def __init__(self, servers):
        self.servers = servers
        self.current_round_robin_index = 0
        self.algorithm = "round_robin" # Default algorithm

    def set_algorithm(self, algorithm_name):
        """Sets the active load balancing algorithm."""
        if algorithm_name in ["round_robin", "least_connections", "ip_hash"]:
            self.algorithm = algorithm_name
            print(f"\nLoad Balancer algorithm set to: {self.algorithm.replace('_', ' ').title()}")
        else:
            print(f"Error: Unknown algorithm '{algorithm_name}'. Using current: {self.algorithm}")

    def get_healthy_servers(self):
        """Returns a list of currently healthy servers."""
        return [s for s in self.servers if s.is_healthy]

    def dispatch_request(self, client_ip, request_id):
        """Dispatches a request based on the selected algorithm."""
        healthy_servers = self.get_healthy_servers()
        if not healthy_servers:
            print(f"No healthy servers available to handle request {request_id} from {client_ip}.")
            return None

        target_server = None
        if self.algorithm == "round_robin":
            target_server = self._round_robin(healthy_servers)
        elif self.algorithm == "least_connections":
            target_server = self._least_connections(healthy_servers)
        elif self.algorithm == "ip_hash":
            target_server = self._ip_hash(client_ip, healthy_servers)
        else:
            print(f"Error: Unknown algorithm '{self.algorithm}'.")
            return None

        if target_server and target_server.handle_request(request_id):
            # Simulate request processing time
            # time.sleep(random.uniform(0.1, 0.5)) # Uncomment to simulate real-time processing
            return target_server
        else:
            # If target_server is None or handle_request failed (e.g., server full)
            print(f"Request {request_id} from {client_ip} could not be dispatched by {self.algorithm.replace('_', ' ').title()}.")
            return None

    def _round_robin(self, healthy_servers):
        """Round Robin algorithm implementation."""
        server_count = len(healthy_servers)
        if server_count == 0:
            return None

        # Ensure index wraps around and points to a healthy server
        for _ in range(server_count): # Try all servers once
            server = healthy_servers[self.current_round_robin_index]
            self.current_round_robin_index = (self.current_round_robin_index + 1) % server_count
            if server.is_healthy:
                return server
        return None # No healthy server found

    def _least_connections(self, healthy_servers):
        """Least Connections algorithm implementation."""
        if not healthy_servers:
            return None
        
        # Find the server with the minimum active connections
        # Using min() with a key for cleaner code
        target_server = min(healthy_servers, key=lambda s: s.active_connections)
        return target_server

    def _ip_hash(self, client_ip, healthy_servers):
        """IP Hash algorithm implementation."""
        server_count = len(healthy_servers)
        if server_count == 0:
            return None

        # Hash the client IP address
        # Using hashlib.sha256 for a robust hash, then convert to int
        hash_object = hashlib.sha256(client_ip.encode())
        hash_value = int(hash_object.hexdigest(), 16)

        # Map hash value to a server index
        server_index = hash_value % server_count
        return healthy_servers[server_index]

    def print_server_status(self):
        """Prints the current status of all servers."""
        print("\n--- Server Status ---")
        for server in self.servers:
            print(server)
        print("---------------------\n")

# --- Simulation ---
if __name__ == "__main__":
    # 1. Setup Servers
    servers = [Server(f"S{i+1}", capacity=random.randint(5, 15)) for i in range(3)]
    lb = LoadBalancer(servers)
    lb.print_server_status()

    # 2. Simulate Round Robin
    print("--- Simulating Round Robin ---")
    lb.set_algorithm("round_robin")
    requests_to_send = 10
    for i in range(requests_to_send):
        client_ip = f"192.168.1.{random.randint(1, 254)}" # Dummy IP
        request_id = f"RR_Req_{i+1}"
        dispatched_server = lb.dispatch_request(client_ip, request_id)
        if dispatched_server:
            # Simulate some requests finishing randomly
            if random.random() < 0.3: # 30% chance a request finishes immediately
                dispatched_server.finish_request(request_id)
        time.sleep(0.05) # Small delay to simulate real-time

    lb.print_server_status()

    # Simulate a server going down for Round Robin
    print("--- Simulating Server Failure (Round Robin) ---")
    servers[0].set_health(False) # S1 goes down
    for i in range(5):
        client_ip = f"192.168.1.{random.randint(1, 254)}"
        request_id = f"RR_Fail_Req_{i+1}"
        lb.dispatch_request(client_ip, request_id)
        time.sleep(0.05)
    lb.print_server_status()
    servers[0].set_health(True) # S1 comes back online

    # Reset server connections for next algorithm
    for s in servers:
        s.active_connections = 0
        s.requests_handled = 0
    lb.current_round_robin_index = 0 # Reset RR index
    lb.print_server_status()

    # 3. Simulate Least Connections
    print("--- Simulating Least Connections ---")
    lb.set_algorithm("least_connections")
    requests_to_send = 15
    active_requests = {} # To track requests for finishing
    for i in range(requests_to_send):
        client_ip = f"192.168.1.{random.randint(1, 254)}"
        request_id = f"LC_Req_{i+1}"
        dispatched_server = lb.dispatch_request(client_ip, request_id)
        if dispatched_server:
            active_requests[request_id] = dispatched_server
        
        # Randomly finish some active requests
        if random.random() < 0.4 and active_requests:
            req_to_finish = random.choice(list(active_requests.keys()))
            server_for_req = active_requests.pop(req_to_finish)
            server_for_req.finish_request(req_to_finish)
        time.sleep(0.05)

    # Finish any remaining active requests
    for req_id, server in active_requests.items():
        server.finish_request(req_id)

    lb.print_server_status()

    # Simulate a server going down for Least Connections
    print("--- Simulating Server Failure (Least Connections) ---")
    servers[1].set_health(False) # S2 goes down
    for i in range(5):
        client_ip = f"192.168.1.{random.randint(1, 254)}"
        request_id = f"LC_Fail_Req_{i+1}"
        lb.dispatch_request(client_ip, request_id)
        time.sleep(0.05)
    lb.print_server_status()
    servers[1].set_health(True) # S2 comes back online

    # Reset server connections for next algorithm
    for s in servers:
        s.active_connections = 0
        s.requests_handled = 0
    lb.print_server_status()

    # 4. Simulate IP Hash
    print("--- Simulating IP Hash ---")
    lb.set_algorithm("ip_hash")
    requests_to_send = 10
    # Use a few distinct client IPs to show stickiness
    client_ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.1", "10.0.0.4", "10.0.0.2", "10.0.0.1", "10.0.0.5", "10.0.0.3", "10.0.0.1"]

    for i, client_ip in enumerate(client_ips):
        request_id = f"IPH_Req_{i+1}"
        print(f"Client {client_ip} sending request {request_id}...")
        dispatched_server = lb.dispatch_request(client_ip, request_id)
        if dispatched_server:
            dispatched_server.finish_request(request_id) # Assume quick finish for IP Hash demo
        time.sleep(0.05)

    lb.print_server_status()

    # Demonstrate stickiness for a specific client
    print("--- Demonstrating IP Hash Stickiness ---")
    specific_client_ip = "192.168.1.100"
    print(f"Client {specific_client_ip} sending multiple requests:")
    for i in range(5):
        request_id = f"Sticky_Req_{i+1}"
        dispatched_server = lb.dispatch_request(specific_client_ip, request_id)
        if dispatched_server:
            print(f"  Request {request_id} from {specific_client_ip} dispatched to {dispatched_server.server_id}")
            dispatched_server.finish_request(request_id)
        time.sleep(0.05)
    lb.print_server_status()

    # Simulate a server going down for IP Hash
    print("--- Simulating Server Failure (IP Hash) ---")
    servers[0].set_health(False) # S1 goes down
    print(f"Server {servers[0].server_id} is down. Clients previously routed to it will fail.")
    for i in range(3):
        client_ip = "10.0.0.1" # This client was likely routed to S1
        request_id = f"IPH_Fail_Req_{i+1}"
        lb.dispatch_request(client_ip, request_id)
        time.sleep(0.05)
    lb.print_server_status()
    servers[0].set_health(True) # S1 comes back online
```

**Explanation of the Code:**

1.  **`Server` Class**:
    *   Represents a single backend server.
    *   `server_id`: Unique identifier.
    *   `active_connections`: Tracks how many requests it's currently processing (crucial for Least Connections).
    *   `requests_handled`: Total requests processed.
    *   `capacity`: Maximum active connections it can handle.
    *   `is_healthy`: A flag to simulate server health (for fault tolerance).
    *   `handle_request()`: Increments `active_connections` and `requests_handled`. Returns `False` if unhealthy or at capacity.
    *   `finish_request()`: Decrements `active_connections`.

2.  **`LoadBalancer` Class**:
    *   `servers`: A list of `Server` objects it manages.
    *   `current_round_robin_index`: Keeps track of the next server for Round Robin.
    *   `algorithm`: Stores the currently active load balancing algorithm.
    *   `set_algorithm()`: Changes the active algorithm.
    *   `get_healthy_servers()`: Filters out unhealthy servers, ensuring requests are only sent to active ones.
    *   `dispatch_request()`: The main method that receives a client IP and request ID, then calls the appropriate internal algorithm method.
    *   `_round_robin()`: Implements the Round Robin logic using the `current_round_robin_index` and modulo arithmetic. It also handles server health.
    *   `_least_connections()`: Finds the server with the minimum `active_connections` among healthy servers.
    *   `_ip_hash()`: Uses `hashlib.sha256` to hash the client IP, converts the hash to an integer, and then uses the modulo operator to map it to a server index.
    *   `print_server_status()`: A utility to display the current state of all servers.

3.  **Simulation (`if __name__ == "__main__":`)**:
    *   Initializes three `Server` instances with random capacities.
    *   Creates a `LoadBalancer` instance.
    *   **Round Robin Simulation**: Sends 10 requests. You'll see requests distributed sequentially. It also demonstrates how the load balancer skips an unhealthy server.
    *   **Least Connections Simulation**: Sends 15 requests. It includes random finishing of requests to simulate dynamic load changes, showing how requests are directed to less busy servers. It also demonstrates handling server failure.
    *   **IP Hash Simulation**: Sends 10 requests using a small set of client IPs to clearly show that the same IP consistently goes to the same server. It also demonstrates the impact of a server failure on clients hashed to that server.

This example provides a clear, hands-on understanding of how each algorithm operates and its implications in a simulated environment.

## Interview Questions

Here's a list of relevant technical interview questions about load balancing algorithms, complete with comprehensive answers.

1.  **What is load balancing, and why is it crucial in modern distributed systems?**
    *   **Answer**: Load balancing is the process of distributing incoming network traffic across multiple backend servers. It's crucial because it addresses several challenges:
        *   **High Availability & Fault Tolerance**: Prevents a single point of failure; if one server fails, traffic is redirected to others.
        *   **Scalability**: Allows applications to handle increased traffic by easily adding more servers (horizontal scaling).
        *   **Performance Optimization**: Prevents server overload, reduces response times, and maximizes throughput by ensuring efficient resource utilization across the server pool.
        *   **Resource Efficiency**: Ensures that no server is idle while others are struggling.

2.  **Explain the Round Robin load balancing algorithm. What are its primary advantages and disadvantages?**
    *   **Answer**: Round Robin distributes client requests to servers in a sequential, rotating manner. Each new request goes to the next server in the list, cycling back to the beginning after reaching the last server.
        *   **Advantages**: Extremely simple to implement and understand, provides a fair and even distribution of requests over time if all requests are uniform and servers have equal capacity.
        *   **Disadvantages**: It's "dumb" to server load; it doesn't consider the actual processing capacity or current workload of servers. This can lead to overloading slower or already busy servers, resulting in performance bottlenecks if requests are heterogeneous. It also doesn't support session persistence.

3.  **When would you choose Least Connections over Round Robin, and what are its limitations?**
    *   **Answer**: You would choose Least Connections when server capacities are heterogeneous, or when the processing time for requests varies significantly. Unlike Round Robin, Least Connections is dynamic; it directs new requests to the server with the fewest active connections. This ensures better resource utilization and prevents individual servers from becoming overloaded.
        *   **Limitations**: It requires the load balancer to track the state (active connections) of each server, adding complexity. It also assumes that all active connections represent an equal amount of load, which isn't always true (e.g., a lightweight API call vs. a heavy ML inference request). If a server gets a few very long-lived connections, it might appear busy even if it could handle many short requests.

4.  **Describe the IP Hash load balancing algorithm. What is its main benefit, and when is it problematic?**
    *   **Answer**: IP Hash uses a hash function on the client's source IP address to determine which backend server should handle the request. The same client IP will always be routed to the same server.
        *   **Main Benefit**: Its primary advantage is **session persistence** (or "sticky sessions"). This is crucial for stateful applications where a user's session data (e.g., shopping cart, login state) is stored on a specific server and needs to be consistently accessed by that same server.
        *   **Problematic When**:
            *   **Uneven Distribution**: If many clients share the same IP (e.g., behind a NAT gateway) or if the client IP distribution is skewed, it can lead to an uneven load distribution, creating "hot spots" on certain servers.
            *   **Server Failure**: If a server fails, all clients that were hashed to that server will lose their session and experience service disruption.
            *   **Scaling Challenges**: Adding or removing servers from the pool can change the modulo operation used in the hash, potentially re-hashing all clients to different servers and breaking existing sticky sessions.

5.  **In the context of serving machine learning models, which load balancing algorithm would you generally prefer and why?**
    *   **Answer**: For serving machine learning models, **Least Connections** is often the most preferred algorithm.
        *   **Why**: ML inference requests can vary significantly in computational complexity and duration (e.g., a simple linear regression prediction vs. a complex deep learning image generation). Least Connections dynamically routes requests to the least busy model server, ensuring that computationally intensive requests don't queue up on an already overloaded server, thus optimizing overall throughput and minimizing latency. Round Robin would be less efficient as it doesn't account for varying inference costs, and IP Hash is typically only needed if there's a specific requirement for client-to-server stickiness for stateful ML models, which is less common for stateless inference.

6.  **What is "sticky sessions," and which load balancing algorithm inherently supports it?**
    *   **Answer**: "Sticky sessions" (or session persistence) refers to the ability of a load balancer to ensure that all requests from a particular client during a session are consistently routed to the same backend server. This is vital for stateful applications where session-specific data is stored on the server and not shared across the entire server pool. The **IP Hash** algorithm inherently supports sticky sessions by always routing requests from the same client IP to the same server based on its hash. Other algorithms can achieve stickiness using cookies, but IP Hash does it by design.

7.  **How do load balancers typically handle server failures with these algorithms?**
    *   **Answer**: Load balancers employ health checks (e.g., ping, HTTP requests to a specific endpoint) to monitor the availability and responsiveness of backend servers.
        *   **Round Robin & Least Connections**: If a server fails a health check, the load balancer marks it as unhealthy and temporarily removes it from the active server pool. New requests will then only be distributed among the remaining healthy servers. Once the failed server recovers and passes health checks, it's added back to the pool.
        *   **IP Hash**: If a server fails, clients whose IP addresses were hashed to that specific server will experience service disruption. The load balancer will stop sending new requests to the failed server, but existing sessions for those clients are broken. When the server recovers, those clients will be re-routed to it. If the server is permanently removed, the load balancer might re-hash clients across the remaining servers, which would break sessions for many clients.

8.  **Can you combine these algorithms or use variations? Give an example.**
    *   **Answer**: Yes, load balancers often offer more sophisticated algorithms or allow combinations.
        *   **Weighted Round Robin/Least Connections**: Assigns a "weight" to each server based on its capacity. A server with a higher weight receives more requests (e.g., a server with weight 2 gets twice as many requests as a server with weight 1 in Round Robin, or is considered "less busy" for Least Connections even with more connections).
        *   **Least Time**: Considers both the number of active connections and the average response time of the server.
        *   **Source IP Hash with Fallback**: Use IP Hash for stickiness, but if the designated server is down or overloaded, fall back to Least Connections or Round Robin.
        *   **Example**: A common setup is **Weighted Least Connections**, where servers with higher processing power are given higher weights, and the load balancer still directs traffic to the server with the fewest active connections, proportionally adjusted by weight.

9.  **What are the implications of using IP Hash when clients are behind a Network Address Translator (NAT)?**
    *   **Answer**: When clients are behind a NAT, multiple internal clients share a single public IP address. If the load balancer uses IP Hash based on the source IP, all these internal clients will appear to come from the same public IP. Consequently, all requests from these different internal clients will be routed to the *same* backend server. This can lead to a severe load imbalance, as one server might become a "hot spot" receiving traffic intended for many users, while other servers remain underutilized. It effectively negates the load balancing aspect for those clients.

10. **How does a load balancer typically determine if a backend server is "healthy"?**
    *   **Answer**: Load balancers use **health checks** to monitor the status of backend servers. These checks can be:
        *   **Ping (ICMP)**: Basic network reachability.
        *   **TCP Health Check**: Attempts to establish a TCP connection to a specific port on the server. If the connection is successful, the server is considered healthy.
        *   **HTTP/HTTPS Health Check**: Sends an HTTP GET request to a specific URL path (e.g., `/healthz` or `/status`) on the server. If the server responds with a success status code (e.g., 200 OK) within a timeout period, it's considered healthy. This is the most common and robust method as it checks the application layer.
        *   **Custom Health Checks**: Some load balancers allow custom scripts or commands to be executed on the server to determine its health.
    *   Health checks are performed periodically, and a server is marked unhealthy if it fails a configured number of consecutive checks. It's marked healthy again if it passes a configured number of consecutive checks.

## Quiz

1.  Which load balancing algorithm distributes requests sequentially to each server in turn?
    A) Least Connections
    B) IP Hash
    C) Round Robin
    D) Weighted Least Time

2.  For an e-commerce application where user session data is stored on individual backend servers, which algorithm is most suitable for maintaining "sticky sessions"?
    A) Round Robin
    B) Least Connections
    C) IP Hash
    D) Random

3.  A major disadvantage of the Round Robin algorithm is:
    A) It requires complex state tracking.
    B) It can lead to uneven load distribution if requests have varying processing times.
    C) It is difficult to implement.
    D) It does not support fault tolerance.

4.  In a scenario where machine learning inference requests vary significantly in computational cost, which load balancing algorithm would likely provide the best overall throughput and lowest latency?
    A) Round Robin
    B) IP Hash
    C) Least Connections
    D) Weighted Round Robin (without considering actual load)

5.  If multiple clients are accessing your service from behind a single corporate firewall (using NAT), and your load balancer uses IP Hash, what is a potential consequence?
    A) All clients will be evenly distributed across all servers.
    B) All clients will be routed to the same backend server, potentially creating a hot spot.
    C) The load balancer will automatically switch to Least Connections.
    D) Session persistence will be guaranteed for each individual client.

---

### Answer Key

1.  **C) Round Robin**
    *   **Explanation**: Round Robin is characterized by its simple, sequential distribution of requests to servers in a rotating fashion.

2.  **C) IP Hash**
    *   **Explanation**: IP Hash ensures that requests from a specific client IP are always routed to the same server, which is essential for maintaining session persistence when session data is server-specific.

3.  **B) It can lead to uneven load distribution if requests have varying processing times.**
    *   **Explanation**: Round Robin is "dumb" to server load. It distributes requests purely sequentially, regardless of how busy a server actually is or how long a request takes to process, which can lead to an imbalance if workloads are not uniform.

4.  **C) Least Connections**
    *   **Explanation**: Least Connections dynamically routes requests to the server with the fewest active connections. This is highly effective for heterogeneous workloads like ML inference, as it ensures that busy servers are not further overloaded, leading to better resource utilization and performance.

5.  **B) All clients will be routed to the same backend server, potentially creating a hot spot.**
    *   **Explanation**: Since all clients behind a NAT share the same public IP address, the IP Hash algorithm will consistently hash that single IP to the same backend server. This means all traffic from those multiple clients will hit that one server, leading to an imbalanced load and a potential hot spot.

## Further Reading

1.  **Nginx Load Balancing**: The official Nginx documentation provides excellent details on how load balancing is implemented in one of the most popular web servers and reverse proxies, including various algorithms and configurations.
    *   [Nginx Load Balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)

2.  **HAProxy Load Balancing Algorithms**: HAProxy is another widely used open-source load balancer. Its documentation offers in-depth explanations of various load balancing algorithms, including the ones discussed here, and their practical implications.
    *   [HAProxy Load Balancing Algorithms](https://www.haproxy.com/blog/the-four-essential-sections-of-an-haproxy-configuration/#section-3-load-balancing-algorithms) (Look for the "Load Balancing Algorithms" section)

3.  **Cloud Provider Load Balancer Documentation (e.g., AWS ELB, Google Cloud Load Balancing, Azure Load Balancer)**: These resources provide practical insights into how load balancing is implemented and managed in large-scale cloud environments, often discussing the trade-offs and use cases for different algorithms.
    *   [AWS Elastic Load Balancing (ELB)](https://aws.amazon.com/elasticloadbalancing/)
    *   [Google Cloud Load Balancing](https://cloud.google.com/load-balancing)
    *   [Azure Load Balancer](https://azure.microsoft.com/en-us/products/load-balancer)