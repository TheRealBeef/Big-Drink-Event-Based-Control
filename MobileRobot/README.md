# ROS 2 Humble + Gazebo

After following intructions you will have ROS2 up and running and Gazebo environement ready to go.

## Set up ROS2 with Gazebo

Only one step here. The command put below will build ROS2 image with a Dockerfile, which will take care of setting it up. It can take a while since it will execute ```apt update``` command and download Gazebo.

```bash
  docker build -t osrf/ros:humble-gazebo .
```

## Run your docker container

After using a `run.sh` script your ros2 is ready to use.

```bash
  . run.sh
```

## Check if it works on your device

The best way to check if everything is fine is to use `turtlesim`.

```bash
  ros2 run turtlesim turtlesim_node
```

If this command doesn't work something is wrong, go to `Troubleshooting` section. If a window with a turtle popped out try to run Gazeebo.

```bash
  ign gazebo shapes.sdf
```

If that worked, everything is fine, you can try to have some fun with Gazebo ( [link to the tutorial](https://gazebosim.org/docs/fortress/tutorials) )

## Troubleshooting

### Known unresolved issues

1. After closing Gazebo window terminal shows an error. Whait till it closes, don't send any report, it seems to work just fine but something weird happens.

### Resolved issues

1. Tourtlesim doesn't work:

* `Error: Can't open display: :0` - close the container, execute `host +`, run container: `. run.sh`.
