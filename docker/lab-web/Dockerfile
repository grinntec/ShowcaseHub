# Use an official Nginx image as a parent image
FROM nginx:latest

# A LABEL is a key-value pair it defines the maintainer of the image
LABEL maintainer="someone@emaildomain"

# Set the working directory in the container to /usr/share/nginx/html
WORKDIR /usr/share/nginx/html

# Copy the specified directory contents into the container at /usr/share/nginx/html
COPY ./src .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
