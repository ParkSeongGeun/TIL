#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <time.h>
#include "html_template.h"

#define PORT 8080
#define BUFFER_SIZE 1024
#define BACKLOG 10

int main() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_size = sizeof(client_addr);
    char buffer[BUFFER_SIZE] = {0};

    // 1. 소켓 생성
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // 2. 서버 주소 설정
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(PORT);

    // 3. 소켓 바인딩
    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("Bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // 4. 연결 대기
    if (listen(server_fd, BACKLOG) == -1) {
        perror("Listen failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d...\n", PORT);

    while (1) {
        client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &addr_size);
        if (client_fd == -1) {
            perror("Accept failed");
            continue;
        }

        // 클라이언트 IP 준비
        unsigned char *ip = (unsigned char *)&client_addr.sin_addr.s_addr;
        char ip_str[50];
        sprintf(ip_str, "%d.%d.%d.%d", ip[0], ip[1], ip[2], ip[3]);

        // 현재 시간 준비
        time_t now = time(NULL);
        char time_str[100];
        strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", localtime(&now));

        // 응답 생성
        char response[4096];
        sprintf(response, HTML_TEMPLATE, ip_str, time_str);

        // HTTP 요청 수신 (생략 가능)
        read(client_fd, buffer, BUFFER_SIZE);

        // 응답 전송
        write(client_fd, response, strlen(response));

        close(client_fd);
    }

    close(server_fd);
    return 0;
}
